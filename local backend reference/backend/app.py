from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import os
import threading
from services.doc_generator import generate_documentation
from services.storage import save_to_csv, save_markdown, sanitize_filename
from services.google_drive import test_connection, upload_file_to_drive, find_or_create_folder, upload_folder_structure, share_with_email, find_or_create_tracking_sheet, append_to_sheet, create_master_doc, update_sheet_status, find_row_by_drive_link
import queue
import time

app = Flask(__name__)

# Configure CORS to allow Vercel frontend
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:3000",     # Local development
            "https://*.vercel.app",       # Vercel preview deployments
            "https://www.nyccode.org",    # Production frontend
            "https://nyccode.org"         # Without www
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Ensure directories exist
os.makedirs('data', exist_ok=True)
os.makedirs('output', exist_ok=True)

# In-memory storage for generated docs (simulates session storage)
documentation_store = {}

# Storage for background processing status
processing_status = {}

# Queue management
processing_queue = queue.Queue()
queue_lock = threading.Lock()
is_processing = False
current_processing_item = None

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'message': 'NYC Code API is running'
    })

@app.route('/api/queue-status', methods=['GET'])
def queue_status():
    """
    Get current queue status
    """
    with queue_lock:
        return jsonify({
            'queue_size': processing_queue.qsize(),
            'is_processing': is_processing,
            'current_processing': current_processing_item['github_url'] if current_processing_item else None
        })

@app.route('/api/test-google-drive', methods=['GET'])
def test_google_drive():
    """
    Test endpoint to verify Google Drive API connection
    """
    try:
        result = test_connection()
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def process_single_repo(github_url, folder_id, repo_name, sheet_id, row_number):
    """
    Process a single repository (called by queue worker)
    """
    md_folder_path = None
    repo_folder_path = None

    try:
        print(f"[Queue Worker] Starting documentation generation for: {github_url}")
        processing_status[github_url]['status'] = 'scraping'

        # Generate documentation using deepwiki scraper
        result = generate_documentation(github_url)

        print(f"[Queue Worker] Documentation generated, creating master doc...")
        processing_status[github_url]['status'] = 'creating_master_doc'

        # Upload folder structure with markdown files
        md_folder_path = result.get('md_folder_path', '')
        repo_folder = result.get('repo_folder', '')

        # Store the full repo folder path for cleanup
        if repo_folder:
            repo_folder_path = os.path.join('output', repo_folder)

        if md_folder_path and os.path.exists(md_folder_path):
            # Get list of .md files
            md_files = [f for f in os.listdir(md_folder_path) if f.endswith('.md')]

            # Create master doc with index and download instructions
            print(f"[Queue Worker] Creating master doc with {len(md_files)} files...")
            master_doc = create_master_doc(repo_name, md_files, folder_id)
            processing_status[github_url]['master_doc_link'] = master_doc['web_view_link']

            # Upload the md folder with all files
            print(f"[Queue Worker] Uploading folder structure from: {md_folder_path}")
            processing_status[github_url]['status'] = 'uploading'
            upload_folder_structure(md_folder_path, folder_id=folder_id)
        else:
            # Fallback: create single file if md_folder not found
            print("[Queue Worker] MD folder not found, creating single combined file...")
            markdown_filepath = save_markdown(github_url, result['markdown'])
            upload_file_to_drive(markdown_filepath, folder_id=folder_id)

        # Update Google Sheet status to "Complete"
        print(f"[Queue Worker] Updating sheet status to Complete for row {row_number}")
        update_sheet_status(sheet_id, row_number, 'Complete')

        processing_status[github_url]['status'] = 'completed'
        print(f"[Queue Worker] Processing completed for: {github_url}")

        # Clean up: Delete markdown files and folder after successful upload
        print(f"[Queue Worker] Cleaning up local files...")
        if repo_folder_path and os.path.exists(repo_folder_path):
            import shutil
            shutil.rmtree(repo_folder_path)
            print(f"[Queue Worker] Deleted folder: {repo_folder_path}")
        else:
            print(f"[Queue Worker] No cleanup needed - folder not found")

    except Exception as e:
        print(f"[Queue Worker] Error: {str(e)}")
        processing_status[github_url]['status'] = 'failed'
        processing_status[github_url]['error'] = str(e)

        # Update sheet status to "Failed" if error occurs
        try:
            update_sheet_status(sheet_id, row_number, 'Failed')
        except:
            pass

        # Clean up even on failure to avoid cluttering disk
        try:
            if repo_folder_path and os.path.exists(repo_folder_path):
                import shutil
                shutil.rmtree(repo_folder_path)
                print(f"[Queue Worker] Cleaned up failed processing folder: {repo_folder_path}")
        except Exception as cleanup_error:
            print(f"[Queue Worker] Cleanup failed: {str(cleanup_error)}")

def queue_worker():
    """
    Queue worker that processes repos sequentially, one at a time
    """
    global is_processing, current_processing_item

    while True:
        try:
            # Wait for item in queue (blocking)
            item = processing_queue.get()

            if item is None:  # Shutdown signal
                break

            with queue_lock:
                is_processing = True
                current_processing_item = item

            github_url = item['github_url']
            folder_id = item['folder_id']
            repo_name = item['repo_name']
            sheet_id = item['sheet_id']
            row_number = item['row_number']

            print(f"[Queue Worker] Processing repo {row_number} from queue: {github_url}")

            # Process this repo
            process_single_repo(github_url, folder_id, repo_name, sheet_id, row_number)

            # Mark task as done
            processing_queue.task_done()

            with queue_lock:
                is_processing = False
                current_processing_item = None

            print(f"[Queue Worker] Finished processing {github_url}. Queue size: {processing_queue.qsize()}")

        except Exception as e:
            print(f"[Queue Worker] Error in worker: {str(e)}")
            processing_queue.task_done()
            with queue_lock:
                is_processing = False
                current_processing_item = None

# Start the queue worker thread when app starts
queue_worker_thread = threading.Thread(target=queue_worker, daemon=True)
queue_worker_thread.start()
print("[App] Queue worker thread started")

@app.route('/api/generate-docs', methods=['POST'])
def generate_docs():
    try:
        data = request.get_json()
        github_url = data.get('githubUrl')

        if not github_url or 'github.com' not in github_url:
            return jsonify({
                'success': False,
                'error': 'Invalid GitHub URL'
            }), 400

        print(f"Creating folder immediately for: {github_url}")

        # Extract repo info
        import re
        pattern = r'github\.com/([^/]+)/([^/]+)'
        match = re.search(pattern, github_url)
        owner = match.group(1)
        repo = match.group(2).replace('.git', '')

        # Step 1: Find or create NYC_Code_Backend folder
        admin_folder = find_or_create_folder('NYC_Code_Backend')
        admin_folder_id = admin_folder['folder_id']

        # Step 2: Create timestamped repo folder name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        folder_name = f"{owner}_{repo}_{timestamp}"

        # Step 3: Create repo folder in Drive immediately
        repo_folder_result = find_or_create_folder(folder_name, admin_folder_id)
        folder_id = repo_folder_result['folder_id']
        drive_link = repo_folder_result['web_view_link']

        print(f"Folder created: {drive_link}")

        # Store folder info for later sharing (will be updated with sheet info when user enters email)
        processing_status[github_url] = {
            'status': 'initializing',
            'folder_id': folder_id,
            'folder_name': folder_name,
            'drive_link': drive_link,
            'repo_name': repo,
            'created_at': datetime.now().isoformat(),
            'sheet_id': None,
            'row_number': None,
            'background_started': False
        }

        return jsonify({
            'success': True,
            'message': 'Folder created, documentation is being generated in the background',
            'folderId': folder_id,
            'driveLink': drive_link
        })

    except Exception as e:
        print(f"Error creating folder: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/share-docs', methods=['POST'])
def share_docs():
    try:
        data = request.get_json()
        github_url = data.get('githubUrl')
        email = data.get('email')

        if not email or '@' not in email:
            return jsonify({
                'success': False,
                'error': 'Invalid email address'
            }), 400

        # Retrieve folder info from processing status
        status_data = processing_status.get(github_url)

        if not status_data:
            return jsonify({
                'success': False,
                'error': 'Folder not found. Please generate documentation first.'
            }), 404

        folder_id = status_data['folder_id']
        drive_link = status_data['drive_link']
        folder_name = status_data['folder_name']

        print(f"Sharing folder {folder_name} with {email}...")

        # Share folder with user's email immediately
        share_with_email(folder_id, email)

        # Find or create NYC_Code_Backend admin folder
        admin_folder = find_or_create_folder('NYC_Code_Backend')
        admin_folder_id = admin_folder['folder_id']

        # Find or create tracking sheet
        tracking_sheet = find_or_create_tracking_sheet(admin_folder_id)
        sheet_id = tracking_sheet['sheet_id']

        # Add row to tracking sheet with status "Processing"
        timestamp = datetime.now().isoformat()
        sheet_result = append_to_sheet(sheet_id, email, github_url, drive_link, timestamp, status='Processing')
        row_number = sheet_result['row_number']
        ticket = sheet_result['ticket']

        # Update processing status with sheet info
        processing_status[github_url]['sheet_id'] = sheet_id
        processing_status[github_url]['row_number'] = row_number
        processing_status[github_url]['ticket'] = ticket

        # Add to processing queue (after user enters email)
        if not status_data.get('background_started', False):
            print(f"[Main] Adding to queue: {github_url} (Ticket: {ticket})")
            repo_name = status_data['repo_name']

            queue_item = {
                'github_url': github_url,
                'folder_id': folder_id,
                'repo_name': repo_name,
                'sheet_id': sheet_id,
                'row_number': row_number,
                'ticket': ticket
            }

            processing_queue.put(queue_item)
            processing_status[github_url]['background_started'] = True
            processing_status[github_url]['queued_at'] = datetime.now().isoformat()

            print(f"[Main] Queue size: {processing_queue.qsize()}, Currently processing: {is_processing}")

        # Save to CSV with Drive link (legacy)
        csv_row = save_to_csv({
            'email': email,
            'github_url': github_url,
            'repo_folder': folder_name,
            'drive_link': drive_link,
            'processing_status': status_data['status'],
            'timestamp': timestamp
        })

        return jsonify({
            'success': True,
            'message': f'Documentation folder shared successfully with {email} via Google Drive',
            'driveLink': drive_link,
            'folderName': folder_name,
            'processingStatus': status_data['status'],
            'sheetRow': csv_row,
            'trackingSheetId': sheet_id,
            'ticket': ticket
        })

    except Exception as e:
        print(f"Error sharing documentation: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

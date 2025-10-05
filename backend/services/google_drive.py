import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# If modifying these scopes, delete the file token.pickle
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/documents'
]

def get_credentials():
    """
    Get or create Google Drive API credentials
    """
    creds = None

    # Use volume path for token if in Docker, otherwise use current directory
    token_dir = os.getenv('TOKEN_DIR', '.')
    token_path = os.path.join(token_dir, 'token.pickle')

    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credentials_path = os.getenv('GOOGLE_CREDENTIALS_PATH', 'client_secret_720052609656-btvogmsj00bk0e6eulc6ec412glnlr2i.apps.googleusercontent.com.json')
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        os.makedirs(token_dir, exist_ok=True)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds

def create_drive_service():
    """
    Create and return Google Drive service
    """
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    return service

def upload_file_to_drive(file_path, file_name=None, folder_id=None):
    """
    Upload a file to Google Drive and return shareable link

    Args:
        file_path: Path to the file to upload
        file_name: Name for the file in Drive (optional, uses original name if not provided)
        folder_id: Google Drive folder ID to upload to (optional)

    Returns:
        dict with file_id and web_view_link
    """
    try:
        service = create_drive_service()

        # Determine file name
        if not file_name:
            file_name = os.path.basename(file_path)

        # Determine MIME type based on file extension
        mime_type = 'text/markdown' if file_path.endswith('.md') else 'application/octet-stream'

        # File metadata
        file_metadata = {
            'name': file_name
        }

        # If folder_id is provided, set the parent folder
        if folder_id:
            file_metadata['parents'] = [folder_id]

        # Upload file
        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()

        # Make file shareable (anyone with link can view)
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        service.permissions().create(
            fileId=file.get('id'),
            body=permission
        ).execute()

        print(f"File uploaded successfully: {file.get('webViewLink')}")

        return {
            'file_id': file.get('id'),
            'web_view_link': file.get('webViewLink')
        }

    except Exception as e:
        raise Exception(f"Failed to upload to Google Drive: {str(e)}")

def create_folder(folder_name, parent_folder_id=None):
    """
    Create a folder in Google Drive and return its ID

    Args:
        folder_name: Name of the folder to create
        parent_folder_id: ID of parent folder (optional)

    Returns:
        dict with folder_id and web_view_link
    """
    try:
        service = create_drive_service()

        # Folder metadata
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        # If parent folder is provided, set it
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]

        # Create folder
        folder = service.files().create(
            body=file_metadata,
            fields='id, webViewLink'
        ).execute()

        # Make folder shareable (anyone with link can view)
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        service.permissions().create(
            fileId=folder.get('id'),
            body=permission
        ).execute()

        print(f"Folder created successfully: {folder.get('webViewLink')}")

        return {
            'folder_id': folder.get('id'),
            'web_view_link': folder.get('webViewLink')
        }

    except Exception as e:
        raise Exception(f"Failed to create folder: {str(e)}")

def find_or_create_folder(folder_name, parent_folder_id=None):
    """
    Find a folder by name or create it if it doesn't exist

    Args:
        folder_name: Name of the folder
        parent_folder_id: ID of parent folder (optional)

    Returns:
        dict with folder_id and web_view_link
    """
    try:
        service = create_drive_service()

        # Search for existing folder
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        if parent_folder_id:
            query += f" and '{parent_folder_id}' in parents"

        results = service.files().list(
            q=query,
            fields="files(id, webViewLink)"
        ).execute()

        items = results.get('files', [])

        if items:
            # Folder exists, return it
            print(f"Folder '{folder_name}' already exists")
            return {
                'folder_id': items[0]['id'],
                'web_view_link': items[0]['webViewLink']
            }
        else:
            # Create new folder
            print(f"Creating new folder '{folder_name}'")
            return create_folder(folder_name, parent_folder_id)

    except Exception as e:
        raise Exception(f"Failed to find or create folder: {str(e)}")

def share_with_email(file_or_folder_id, email):
    """
    Share a file or folder with a specific email address

    Args:
        file_or_folder_id: ID of the file or folder to share
        email: Email address to share with

    Returns:
        dict with success status
    """
    try:
        service = create_drive_service()

        permission = {
            'type': 'user',
            'role': 'reader',
            'emailAddress': email
        }

        service.permissions().create(
            fileId=file_or_folder_id,
            body=permission,
            sendNotificationEmail=True
        ).execute()

        print(f"Shared with {email} successfully")

        return {
            'success': True,
            'message': f'Shared with {email}'
        }

    except Exception as e:
        raise Exception(f"Failed to share with email: {str(e)}")

def upload_folder_structure(local_folder_path, folder_id=None):
    """
    Upload files from a folder to an existing Google Drive folder

    Args:
        local_folder_path: Path to local folder containing files
        folder_id: ID of the Drive folder to upload files to (optional)

    Returns:
        dict with uploaded files info
    """
    try:
        # Upload all files in the local folder
        uploaded_files = []
        if os.path.exists(local_folder_path):
            for filename in os.listdir(local_folder_path):
                file_path = os.path.join(local_folder_path, filename)
                if os.path.isfile(file_path):
                    file_result = upload_file_to_drive(file_path, filename, folder_id)
                    uploaded_files.append(file_result)
                    print(f"Uploaded {filename}")

        return {
            'uploaded_files': uploaded_files,
            'count': len(uploaded_files)
        }

    except Exception as e:
        raise Exception(f"Failed to upload folder structure: {str(e)}")

def create_google_sheet(sheet_name, parent_folder_id=None):
    """
    Create a Google Sheet and return its ID

    Args:
        sheet_name: Name of the sheet
        parent_folder_id: ID of parent folder (optional)

    Returns:
        dict with sheet_id and web_view_link
    """
    try:
        service = create_drive_service()

        # Sheet metadata
        file_metadata = {
            'name': sheet_name,
            'mimeType': 'application/vnd.google-apps.spreadsheet'
        }

        # If parent folder is provided, set it
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]

        # Create sheet
        sheet = service.files().create(
            body=file_metadata,
            fields='id, webViewLink'
        ).execute()

        sheet_id = sheet.get('id')

        # Initialize sheet with headers
        from googleapiclient.discovery import build
        sheets_service = build('sheets', 'v4', credentials=get_credentials())

        # Add headers
        sheets_service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range='A1:F1',
            valueInputOption='RAW',
            body={
                'values': [['Email', 'Repository URL', 'Google Drive Link', 'Timestamp', 'Status', 'Ticket']]
            }
        ).execute()

        # Format headers (bold)
        sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=sheet_id,
            body={
                'requests': [{
                    'repeatCell': {
                        'range': {
                            'sheetId': 0,
                            'startRowIndex': 0,
                            'endRowIndex': 1
                        },
                        'cell': {
                            'userEnteredFormat': {
                                'textFormat': {'bold': True}
                            }
                        },
                        'fields': 'userEnteredFormat.textFormat.bold'
                    }
                }]
            }
        ).execute()

        print(f"Google Sheet created: {sheet.get('webViewLink')}")

        return {
            'sheet_id': sheet_id,
            'web_view_link': sheet.get('webViewLink')
        }

    except Exception as e:
        raise Exception(f"Failed to create Google Sheet: {str(e)}")

def append_to_sheet(sheet_id, email, repo_url, drive_link, timestamp, status='Processing'):
    """
    Append a row to the tracking sheet with status and ticket number

    Args:
        sheet_id: ID of the Google Sheet
        email: User's email
        repo_url: GitHub repository URL
        drive_link: Google Drive link to the repo folder
        timestamp: Timestamp of the request
        status: Status of processing (default: 'Processing')

    Returns:
        dict with success status and row number
    """
    try:
        sheets_service = build('sheets', 'v4', credentials=get_credentials())

        # First, get current data to calculate ticket number
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range='E:E'  # Status column
        ).execute()

        values = result.get('values', [])

        # Count "Processing" entries (excluding header)
        processing_count = 0
        if len(values) > 1:  # Skip header row
            for row in values[1:]:
                if row and len(row) > 0 and row[0] == 'Processing':
                    processing_count += 1

        # Ticket is the count of processing items before this one
        ticket_number = processing_count

        # Append row with status and ticket
        append_result = sheets_service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range='A:F',
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body={
                'values': [[email, repo_url, drive_link, timestamp, status, ticket_number]]
            }
        ).execute()

        # Get the row number that was just added
        updated_range = append_result.get('updates', {}).get('updatedRange', '')
        row_number = int(updated_range.split('!')[1].split(':')[0].replace('A', ''))

        print(f"Added row {row_number} to tracking sheet: {email}, {repo_url}, Status: {status}, Ticket: {ticket_number}")

        return {
            'success': True,
            'message': 'Row added to tracking sheet',
            'row_number': row_number,
            'ticket': ticket_number
        }

    except Exception as e:
        raise Exception(f"Failed to append to sheet: {str(e)}")

def update_sheet_status(sheet_id, row_number, status='Complete'):
    """
    Update the status of a specific row in the tracking sheet

    Args:
        sheet_id: ID of the Google Sheet
        row_number: Row number to update
        status: New status (default: 'Complete')

    Returns:
        dict with success status
    """
    try:
        sheets_service = build('sheets', 'v4', credentials=get_credentials())

        # Update the status cell (column E)
        sheets_service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range=f'E{row_number}',
            valueInputOption='RAW',
            body={
                'values': [[status]]
            }
        ).execute()

        print(f"Updated row {row_number} status to: {status}")

        return {
            'success': True,
            'message': f'Status updated to {status}'
        }

    except Exception as e:
        raise Exception(f"Failed to update sheet status: {str(e)}")

def find_row_by_drive_link(sheet_id, drive_link):
    """
    Find the row number for a specific drive link

    Args:
        sheet_id: ID of the Google Sheet
        drive_link: Google Drive link to search for

    Returns:
        Row number if found, None otherwise
    """
    try:
        sheets_service = build('sheets', 'v4', credentials=get_credentials())

        # Get all data from column C (Google Drive Link)
        result = sheets_service.spreadsheets().values().get(
            spreadsheetId=sheet_id,
            range='C:C'
        ).execute()

        values = result.get('values', [])

        # Search for the drive link (starting from row 2 to skip header)
        for i, row in enumerate(values[1:], start=2):
            if row and len(row) > 0 and row[0] == drive_link:
                return i

        return None

    except Exception as e:
        raise Exception(f"Failed to find row: {str(e)}")

def find_or_create_tracking_sheet(parent_folder_id):
    """
    Find or create the NYC_Code_Tracking sheet in the admin folder

    Args:
        parent_folder_id: ID of the parent folder

    Returns:
        dict with sheet_id and web_view_link
    """
    try:
        service = create_drive_service()

        # Search for existing sheet
        query = f"name='NYC_Code_Tracking' and mimeType='application/vnd.google-apps.spreadsheet' and trashed=false and '{parent_folder_id}' in parents"

        results = service.files().list(
            q=query,
            fields="files(id, webViewLink)"
        ).execute()

        items = results.get('files', [])

        if items:
            # Sheet exists, return it
            print(f"Tracking sheet already exists")
            return {
                'sheet_id': items[0]['id'],
                'web_view_link': items[0]['webViewLink']
            }
        else:
            # Create new sheet
            print(f"Creating new tracking sheet")
            return create_google_sheet('NYC_Code_Tracking', parent_folder_id)

    except Exception as e:
        raise Exception(f"Failed to find or create tracking sheet: {str(e)}")

def create_master_doc(repo_name, md_files, parent_folder_id=None):
    """
    Create a master Google Doc with index and download instructions

    Args:
        repo_name: Name of the repository
        md_files: List of markdown file names
        parent_folder_id: ID of parent folder (optional)

    Returns:
        dict with doc_id and web_view_link
    """
    try:
        service = create_drive_service()

        # Doc metadata
        file_metadata = {
            'name': f'{repo_name}_Master_Index',
            'mimeType': 'application/vnd.google-apps.document'
        }

        # If parent folder is provided, set it
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]

        # Create doc
        doc = service.files().create(
            body=file_metadata,
            fields='id, webViewLink'
        ).execute()

        doc_id = doc.get('id')

        # Build document content
        docs_service = build('docs', 'v1', credentials=get_credentials())

        # Prepare content
        requests = []

        # Download instructions
        download_instructions = """HOW TO DOWNLOAD .MD FILES FROM GOOGLE DRIVE

Step 1: Locate the Files
- All .md (Markdown) files are listed in this folder
- Each file represents a different part of the repository documentation

Step 2: Download Individual Files
- Right-click on any .md file
- Select "Download" from the menu
- The file will be saved to your Downloads folder

Step 3: Download All Files at Once
- Go back to the main folder view
- Select all .md files (hold Ctrl/Cmd and click each file)
- Right-click and select "Download"
- Files will be downloaded as a .zip file

Step 4: Open .md Files
- Use any text editor (Notepad, VSCode, Sublime Text, etc.)
- Or use a Markdown viewer for formatted viewing
- Recommended tools: VSCode, Typora, or online Markdown viewers

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""

        # Repository index
        index_content = f"REPOSITORY: {repo_name}\n\nFILE INDEX:\n\n"
        for i, md_file in enumerate(md_files, 1):
            index_content += f"{i}. {md_file}\n"

        index_content += f"\n\nTotal Files: {len(md_files)}\n"

        full_content = download_instructions + index_content

        # Insert content
        requests.append({
            'insertText': {
                'location': {'index': 1},
                'text': full_content
            }
        })

        # Format the title
        requests.append({
            'updateParagraphStyle': {
                'range': {
                    'startIndex': 1,
                    'endIndex': len('HOW TO DOWNLOAD .MD FILES FROM GOOGLE DRIVE') + 1
                },
                'paragraphStyle': {
                    'namedStyleType': 'HEADING_1'
                },
                'fields': 'namedStyleType'
            }
        })

        # Execute all requests
        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests}
        ).execute()

        print(f"Master doc created: {doc.get('webViewLink')}")

        return {
            'doc_id': doc_id,
            'web_view_link': doc.get('webViewLink')
        }

    except Exception as e:
        raise Exception(f"Failed to create master doc: {str(e)}")

def test_connection():
    """
    Test Google Drive API connection
    """
    try:
        service = create_drive_service()

        # List first 10 files to test connection
        results = service.files().list(
            pageSize=10,
            fields="nextPageToken, files(id, name)"
        ).execute()

        items = results.get('files', [])

        if not items:
            return {
                'success': True,
                'message': 'Connected to Google Drive successfully (no files found)',
                'files': []
            }
        else:
            return {
                'success': True,
                'message': f'Connected to Google Drive successfully. Found {len(items)} files.',
                'files': [{'name': item['name'], 'id': item['id']} for item in items]
            }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

import csv
import os
from datetime import datetime
import re

# CSV file path for storing user data
CSV_FILE = 'data/submissions.csv'
OUTPUT_DIR = 'output'

def sanitize_filename(url):
    """
    Create a safe filename from GitHub URL
    """
    # Extract repo name from URL
    pattern = r'github\.com/([^/]+)/([^/]+)'
    match = re.search(pattern, url)

    if match:
        owner = match.group(1)
        repo = match.group(2).replace('.git', '')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{owner}_{repo}_{timestamp}.md"
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"documentation_{timestamp}.md"

def save_markdown(github_url, markdown_content):
    """
    Save markdown documentation to a file and return filepath
    """
    try:
        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Generate filename
        filename = sanitize_filename(github_url)
        filepath = os.path.join(OUTPUT_DIR, filename)

        # Write markdown to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        print(f"Markdown saved to: {filepath}")
        return filepath

    except Exception as e:
        raise Exception(f"Failed to save markdown: {str(e)}")

def save_to_csv(data):
    """
    Save submission data to CSV file (simulates Google Sheets)
    Data format: email, github_url, deepwiki_url, repo_folder, drive_link, timestamp
    """
    try:
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)

        # Check if file exists to determine if we need headers
        file_exists = os.path.isfile(CSV_FILE)

        # Prepare row data
        row = {
            'email': data.get('email', ''),
            'github_url': data.get('github_url', ''),
            'deepwiki_url': data.get('deepwiki_url', ''),
            'repo_folder': data.get('repo_folder', ''),
            'drive_link': data.get('drive_link', ''),
            'timestamp': data.get('timestamp', datetime.now().isoformat())
        }

        # Write to CSV
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['email', 'github_url', 'deepwiki_url', 'repo_folder', 'drive_link', 'timestamp']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header if file is new
            if not file_exists:
                writer.writeheader()

            # Write data row
            writer.writerow(row)

        print(f"Data saved to CSV: {CSV_FILE}")
        return row

    except Exception as e:
        raise Exception(f"Failed to save to CSV: {str(e)}")

def read_csv():
    """
    Read all submissions from CSV file
    """
    try:
        if not os.path.isfile(CSV_FILE):
            return []

        submissions = []
        with open(CSV_FILE, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                submissions.append(row)

        return submissions

    except Exception as e:
        raise Exception(f"Failed to read CSV: {str(e)}")

def get_submission_by_email(email):
    """
    Get all submissions for a specific email
    """
    try:
        submissions = read_csv()
        return [s for s in submissions if s['email'] == email]

    except Exception as e:
        raise Exception(f"Failed to get submissions: {str(e)}")

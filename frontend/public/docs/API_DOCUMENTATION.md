# API Documentation

## Overview

NYC Code API converts any public GitHub repository into comprehensive markdown documentation and delivers it via Google Drive. No authentication required.

---

## Quick Start

### Example Request

```bash
curl -X POST https://nyccode.org/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"github_url": "https://github.com/psf/requests"}'
```

### Example Response

```json
{
  "success": true,
  "drive_link": "https://drive.google.com/drive/folders/xxx",
  "ticket": "0",
  "status": "processing",
  "estimated_time": "5-30 minutes"
}
```

---

## API Endpoints

### 1. Generate Documentation

**Endpoint**: `POST /api/v1/generate`

**Description**: Generate markdown documentation for any public GitHub repository.

**Request Body**:
```json
{
  "github_url": "https://github.com/owner/repository"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Documentation is being generated...",
  "drive_link": "https://drive.google.com/drive/folders/xxx",
  "folder_name": "owner_repository_20251009_143805",
  "ticket": "0",
  "status": "processing",
  "queue_position": 1,
  "estimated_time": "5-30 minutes depending on repository size"
}
```

**Response Fields**:
- `success` (boolean): Whether the request was successful
- `drive_link` (string): Google Drive folder URL with all documentation
- `folder_name` (string): Name of the created folder
- `ticket` (string): Queue ticket number for tracking
- `status` (string): Current processing status
- `queue_position` (number): Position in processing queue
- `estimated_time` (string): Estimated completion time

**Error Response**:
```json
{
  "success": false,
  "error": "Invalid GitHub URL. Please provide a valid public GitHub repository URL.",
  "example": "https://github.com/openai/openai-python"
}
```

---

### 2. Check Status

**Endpoint**: `GET /api/v1/status`

**Description**: Check the processing status of a documentation request.

**Query Parameters**:
- `github_url` (required): The GitHub URL used in the generate request

**Example Request**:
```bash
curl "https://nyccode.org/api/v1/status?github_url=https://github.com/psf/requests"
```

**Response**:
```json
{
  "success": true,
  "status": "completed",
  "drive_link": "https://drive.google.com/drive/folders/xxx",
  "folder_name": "psf_requests_20251009_143805",
  "ticket": "0",
  "created_at": "2025-10-09T14:38:08.131127",
  "master_doc_link": "https://docs.google.com/document/d/xxx",
  "error": null
}
```

**Status Values**:
- `processing`: Documentation is being generated
- `completed`: All files ready in Google Drive
- `failed`: Processing failed (check `error` field)

---

### 3. API Documentation

**Endpoint**: `GET /api/v1/docs`

**Description**: Get full API specification in JSON format.

**Example Request**:
```bash
curl https://nyccode.org/api/v1/docs
```

**Response**: Complete API specification including all endpoints, parameters, and examples.

---

## Code Examples

### Python

```python
import requests
import time

# Generate documentation
def generate_docs(github_url):
    response = requests.post(
        'https://nyccode.org/api/v1/generate',
        json={'github_url': github_url}
    )
    return response.json()

# Check status
def check_status(github_url):
    response = requests.get(
        'https://nyccode.org/api/v1/status',
        params={'github_url': github_url}
    )
    return response.json()

# Complete workflow
github_url = 'https://github.com/psf/requests'

# Step 1: Generate
result = generate_docs(github_url)
print(f"✓ Drive Link: {result['drive_link']}")
print(f"✓ Ticket: {result['ticket']}")

# Step 2: Poll status until complete
while True:
    status = check_status(github_url)
    print(f"Status: {status['status']}")

    if status['status'] == 'completed':
        print(f"✓ Complete! Master Doc: {status['master_doc_link']}")
        break
    elif status['status'] == 'failed':
        print(f"✗ Failed: {status.get('error')}")
        break

    time.sleep(30)  # Check every 30 seconds
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

async function generateDocs(githubUrl) {
  const response = await axios.post('https://nyccode.org/api/v1/generate', {
    github_url: githubUrl
  });
  return response.data;
}

async function checkStatus(githubUrl) {
  const response = await axios.get('https://nyccode.org/api/v1/status', {
    params: { github_url: githubUrl }
  });
  return response.data;
}

// Complete workflow
(async () => {
  const githubUrl = 'https://github.com/psf/requests';

  // Step 1: Generate
  const result = await generateDocs(githubUrl);
  console.log('✓ Drive Link:', result.drive_link);

  // Step 2: Poll status
  const pollStatus = setInterval(async () => {
    const status = await checkStatus(githubUrl);
    console.log('Status:', status.status);

    if (status.status === 'completed') {
      console.log('✓ Complete!');
      clearInterval(pollStatus);
    } else if (status.status === 'failed') {
      console.error('✗ Failed');
      clearInterval(pollStatus);
    }
  }, 30000); // Check every 30 seconds
})();
```

### JavaScript (Browser/React)

```javascript
async function generateDocs() {
  const githubUrl = document.getElementById('github-url').value;

  // Step 1: Generate
  const response = await fetch('https://nyccode.org/api/v1/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ github_url: githubUrl })
  });

  const data = await response.json();

  // Show drive link immediately
  document.getElementById('drive-link').innerHTML =
    `<a href="${data.drive_link}" target="_blank">Open Google Drive Folder</a>`;

  // Step 2: Poll status
  pollStatus(githubUrl);
}

function pollStatus(githubUrl) {
  const interval = setInterval(async () => {
    const response = await fetch(
      `https://nyccode.org/api/v1/status?github_url=${encodeURIComponent(githubUrl)}`
    );
    const data = await response.json();

    document.getElementById('status').textContent = data.status;

    if (data.status === 'completed' || data.status === 'failed') {
      clearInterval(interval);
    }
  }, 30000);
}
```

---

## API Specifications

| Property | Value |
|----------|-------|
| **Base URL** | `https://nyccode.org` |
| **Protocol** | HTTPS |
| **Authentication** | None |
| **Rate Limiting** | None |
| **CORS** | Enabled |
| **Request Format** | JSON |
| **Response Format** | JSON |

---

## Response Codes

| Code | Description |
|------|-------------|
| `200` | Success |
| `400` | Bad Request (invalid parameters) |
| `404` | Not Found (no processing found for URL) |
| `500` | Internal Server Error |

---

## Processing Timeline

1. **Instant** (0s): Drive folder created, link returned
2. **Processing** (5-30min): Documentation being generated
3. **Complete**: All files available in Google Drive

---

## Output Structure

Each request creates a Google Drive folder containing:

```
📁 owner_repository_20251009_143805/
├── 📄 repository_Master_Index.docx    # Download instructions & file index
├── 📄 1-overview.md                   # Documentation files
├── 📄 2-installation.md
├── 📄 3-quickstart.md
├── 📄 4-api-reference.md
└── 📄 ...
```

---

## Best Practices

### 1. Save the Drive Link Immediately
The Drive link is available instantly. Save it before processing completes.

### 2. Implement Status Polling
Poll the status endpoint every 30-60 seconds to track progress.

### 3. Handle Long Processing Times
Large repositories may take 20-30 minutes. Set appropriate timeouts.

### 4. Cache Results
Store drive links to avoid regenerating documentation for the same repository.

### 5. Error Handling
Always check the `success` field and handle errors gracefully.

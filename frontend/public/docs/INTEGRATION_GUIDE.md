# App Integration Guide

## Context
You are integrating the NYC Code API into an existing application. This guide provides architecture patterns, code examples, and implementation considerations.

---

## Architecture Patterns

### Pattern 1: Simple Request-Response (Best for CLIs)

```python
import requests

def generate_and_wait(github_url):
    response = requests.post(
        'https://nyccode.org/api/v1/generate',
        json={'github_url': github_url}
    )
    data = response.json()
    return data['drive_link']

# User gets link instantly, can check later
drive_link = generate_and_wait('https://github.com/psf/requests')
print(f"Your docs: {drive_link}")
```

**Pros**:
- Simple implementation
- User gets link immediately
- No polling logic needed

**Cons**:
- User must manually check when docs are ready
- No status updates

---

### Pattern 2: Background Polling (Best for Web Apps)

```javascript
class DocsGenerator {
  constructor(apiUrl = 'https://nyccode.org') {
    this.apiUrl = apiUrl;
    this.pollInterval = null;
  }

  async generate(githubUrl, onStatusUpdate) {
    const response = await fetch(`${this.apiUrl}/api/v1/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ github_url: githubUrl })
    });

    const data = await response.json();

    onStatusUpdate({
      status: 'processing',
      driveLink: data.drive_link,
      ticket: data.ticket
    });

    this.startPolling(githubUrl, onStatusUpdate);
  }

  startPolling(githubUrl, onStatusUpdate) {
    this.pollInterval = setInterval(async () => {
      const response = await fetch(
        `${this.apiUrl}/api/v1/status?github_url=${encodeURIComponent(githubUrl)}`
      );
      const data = await response.json();

      onStatusUpdate(data);

      if (data.status === 'completed' || data.status === 'failed') {
        this.stopPolling();
      }
    }, 30000);
  }

  stopPolling() {
    if (this.pollInterval) {
      clearInterval(this.pollInterval);
    }
  }
}
```

---

## Critical Constraints to Handle

### 1. Sequential Processing (FIFO Queue)

**Constraint**: The backend processes one repository at a time.

**How to Handle**:
```javascript
const response = await generateDocs(githubUrl);
console.log(`You are #${response.queue_position} in queue`);

const estimatedWait = response.queue_position * 15; // Assume 15 min per repo
console.log(`Estimated wait: ${estimatedWait} minutes`);
```

**User Messaging**:
- ✓ "You are #3 in queue. Estimated wait: 45 minutes"
- ✗ "Processing will take 5-10 minutes" (misleading if queue is long)

---

### 2. Long Processing Time (5-30 minutes)

**Constraint**: Documentation generation takes significant time.

**User Messaging**:
- ✓ "Processing takes 5-30 minutes. Here's your Drive link to check later."
- ✓ "Processing... (Est. 15 min remaining)"
- ✗ "Almost done!" (when it's been 2 minutes of 20)

---

### 3. No Persistent State (In-Memory Queue)

**Constraint**: Server restart clears processing queue and status.

**User Messaging**:
- ✓ "Save your Drive link! You can always access it even if status is unavailable."
- ✗ "We'll email you when it's ready" (can't guarantee notification)

---

### 4. Public File Access

**Constraint**: All generated files are publicly accessible via Drive link.

**User Messaging**:
- ✓ "All documentation files are publicly accessible via the Drive link"
- ✓ "Do not use with private/sensitive repositories"

---

## Database Schema Recommendations

```sql
CREATE TABLE documentation_requests (
    id SERIAL PRIMARY KEY,
    github_url VARCHAR(500) NOT NULL,
    drive_link VARCHAR(500),
    folder_name VARCHAR(255),
    ticket VARCHAR(50),
    status VARCHAR(50),
    master_doc_link VARCHAR(500),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    error_message TEXT,

    INDEX idx_github_url (github_url),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);
```

---

## Complete Example: React Hook

```javascript
import { useState, useCallback } from 'react';

function useDocsGenerator() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);

  const generate = useCallback(async (githubUrl) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('https://nyccode.org/api/v1/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ github_url: githubUrl })
      });

      const data = await response.json();

      if (!data.success) {
        throw new Error(data.error);
      }

      setResult(data);
      setLoading(false);
      pollStatus(githubUrl);

    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  }, []);

  const pollStatus = useCallback((githubUrl) => {
    const interval = setInterval(async () => {
      const response = await fetch(
        `https://nyccode.org/api/v1/status?github_url=${encodeURIComponent(githubUrl)}`
      );
      const data = await response.json();

      setStatus(data);

      if (data.status === 'completed' || data.status === 'failed') {
        clearInterval(interval);
      }
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  return { generate, loading, result, status, error };
}
```

---

## Performance Optimization

### 1. Debounce Status Checks
Don't poll too frequently - 30-60 seconds is optimal

### 2. Cache Drive Links
Store links locally to avoid redundant API calls

### 3. Handle Network Errors
Implement retry logic with exponential backoff

### 4. Show Progress Indicators
Keep users informed during long processing times

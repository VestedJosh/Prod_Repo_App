import React, { useState } from 'react';
import './ApiDocs.css';

function ApiDocs() {
  const [copied, setCopied] = useState(false);

  const llmInstructions = `INSTRUCTIONS FOR LLM ASSISTANTS:

When a user asks you to help them use the NYC Code API, follow these steps:

STEP 1: Check what tools are available on their system
-------------------------------------------------------
Run these commands to check:
- Python: python --version  OR  python3 --version
- Node.js: node --version
- curl: curl --version

STEP 2: Create the appropriate script based on available tools
--------------------------------------------------------------

IF Python is available:
-----------------------
Create a file called "nyc_code_generator.py" with this code:

import requests
import json

# Get user input
github_url = input("Enter GitHub repository URL: ")
email = input("Enter your email: ")

# Call the API
print("\\nGenerating documentation...")
response = requests.post(
    'https://nyccode.org/api/v1/generate',
    json={
        'github_url': github_url,
        'email': email
    }
)

result = response.json()

if result.get('success'):
    drive_link = result['drive_link']

    # Save to file
    with open('nyc_code_result.txt', 'w') as f:
        f.write(f"GitHub Repository: {github_url}\\n")
        f.write(f"Email: {email}\\n")
        f.write(f"Drive Link: {drive_link}\\n")
        f.write(f"Status: {result['status']}\\n")
        f.write(f"Estimated Time: {result['estimated_time']}\\n")

    print(f"\\n✓ Success! Drive link saved to 'nyc_code_result.txt'")
    print(f"\\nDrive Link: {drive_link}")
    print(f"Email shared with: {email}")
    print(f"Status: {result['status']}")
    print(f"Estimated Time: {result['estimated_time']}")
else:
    print(f"\\n✗ Error: {result.get('error', 'Unknown error')}")

Then tell the user: "Run this with: python nyc_code_generator.py"


IF Node.js is available (but not Python):
------------------------------------------
Create a file called "nyc_code_generator.js" with this code:

const readline = require('readline');
const fs = require('fs');

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

rl.question('Enter GitHub repository URL: ', (github_url) => {
    rl.question('Enter your email: ', (email) => {
        rl.close();

        console.log('\\nGenerating documentation...');

        fetch('https://nyccode.org/api/v1/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                github_url: github_url,
                email: email
            })
        })
        .then(res => res.json())
        .then(result => {
            if (result.success) {
                const output = \`GitHub Repository: \${github_url}
Email: \${email}
Drive Link: \${result.drive_link}
Status: \${result.status}
Estimated Time: \${result.estimated_time}\`;

                fs.writeFileSync('nyc_code_result.txt', output);

                console.log('\\n✓ Success! Drive link saved to nyc_code_result.txt');
                console.log(\`\\nDrive Link: \${result.drive_link}\`);
                console.log(\`Email shared with: \${email}\`);
                console.log(\`Status: \${result.status}\`);
                console.log(\`Estimated Time: \${result.estimated_time}\`);
            } else {
                console.log(\`\\n✗ Error: \${result.error || 'Unknown error'}\`);
            }
        })
        .catch(err => console.error('Error:', err));
    });
});

Then tell the user: "Run this with: node nyc_code_generator.js"


IF curl is available (but not Python or Node.js):
-------------------------------------------------
Create a file called "nyc_code_generator.sh" (Linux/Mac) or "nyc_code_generator.bat" (Windows)

For Linux/Mac (.sh):
#!/bin/bash
read -p "Enter GitHub repository URL: " GITHUB_URL
read -p "Enter your email: " EMAIL
curl -X POST https://nyccode.org/api/v1/generate \\
  -H "Content-Type: application/json" \\
  -d "{\\"github_url\\": \\"\$GITHUB_URL\\", \\"email\\": \\"\$EMAIL\\"}" \\
  -o nyc_code_result.json
echo "Result saved to nyc_code_result.json"
cat nyc_code_result.json

For Windows (.bat):
@echo off
set /p GITHUB_URL="Enter GitHub repository URL: "
set /p EMAIL="Enter your email: "
curl -X POST https://nyccode.org/api/v1/generate -H "Content-Type: application/json" -d "{\\"github_url\\": \\"%GITHUB_URL%\\", \\"email\\": \\"%EMAIL%\\"}" -o nyc_code_result.json
echo Result saved to nyc_code_result.json
type nyc_code_result.json
pause

Then tell the user how to run it based on their OS.


IF NONE are available AND user is on Windows:
---------------------------------------------
Create these two files:

FILE 1: nyc_code_launcher.bat
@echo off
echo Opening NYC Code in your browser...
echo.
echo You'll get your Google Drive link in about 30 seconds after submitting!
echo The link will appear on screen - copy it and save it.
echo.
start https://nyccode.org
pause

FILE 2: README.txt
NYC Code - Quick Start Guide
============================

Since Python, Node.js, and curl are not installed on your system,
we've created a simple launcher that will open the NYC Code website.

INSTRUCTIONS:
1. Double-click "nyc_code_launcher.bat"
2. Your browser will open to https://nyccode.org
3. Enter your GitHub repository URL
4. Click "Generate Documentation"
5. After 30 seconds, enter your email
6. Copy the Google Drive link that appears
7. Save the link somewhere safe!

The documentation will continue processing in the background.
You can check the Drive folder anytime to see the completed docs.

ALTERNATIVE: Install Python, Node.js, or curl
----------------------------------------------
If you want to use the API directly from command line:
- Python: https://python.org/downloads
- Node.js: https://nodejs.org
- curl: Included in Windows 10+ (type 'curl' in Command Prompt)

Then tell the user:
"I've created a browser launcher for you. Double-click 'nyc_code_launcher.bat'
and read 'README.txt' for instructions. You'll get your Drive link in 30 seconds!"


STEP 3: After creating the script
---------------------------------
Always remind the user:
1. The Drive link is available immediately
2. Documentation takes 5-30 minutes to fully generate
3. They can access the folder anytime using the Drive link
4. Large repositories take longer to process`;

  const handleCopyLLM = () => {
    navigator.clipboard.writeText(llmInstructions).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <div className="api-docs">
      <div className="api-container">
        <h1>NYC Code API Documentation</h1>
        <p className="api-subtitle">
          Generate markdown documentation for any public GitHub repository
        </p>

        <section className="api-section llm-prompt-section">
          <div className="llm-header">
            <div>
              <h2>🤖 LLM Getting Started Assistant</h2>
              <p className="llm-subtitle">For AI assistants helping users get started with NYC Code API</p>
            </div>
            <button
              className={`copy-button ${copied ? 'copied' : ''}`}
              onClick={handleCopyLLM}
            >
              {copied ? '✓ Copied!' : 'Copy Instructions'}
            </button>
          </div>

          <div className="code-block llm-instructions">
            <pre>{llmInstructions}</pre>
          </div>
        </section>

        <section className="api-section">
          <h2>Quick Start</h2>
          <p>Get started with the NYC Code API in seconds. No authentication required.</p>

          <div className="example-note">
            <strong>Try it now:</strong> Copy this command and run it in your terminal.
            Replace the GitHub URL and email with your own values.
          </div>

          <div className="code-block">
            <pre>{`curl -X POST https://nyccode.org/api/v1/generate \\
  -H "Content-Type: application/json" \\
  -d '{
    "github_url": "https://github.com/openai/openai-python",
    "email": "user@example.com"
  }'`}</pre>
          </div>

          <div className="example-variations">
            <h4>Example GitHub URLs you can try:</h4>
            <ul>
              <li><code>https://github.com/psf/requests</code> - Popular Python HTTP library</li>
              <li><code>https://github.com/facebook/react</code> - React JavaScript library</li>
              <li><code>https://github.com/tensorflow/tensorflow</code> - Machine learning framework</li>
              <li><code>https://github.com/microsoft/vscode</code> - VS Code editor</li>
            </ul>
          </div>
        </section>

        <section className="api-section">
          <h2>API Endpoints</h2>

          <div className="endpoint">
            <h3><span className="method post">POST</span> /api/v1/generate</h3>
            <p>Generate markdown documentation for a GitHub repository and share it with your email</p>

            <h4>Request Body:</h4>
            <div className="code-block">
              <pre>{`{
  "github_url": "https://github.com/owner/repository",
  "email": "user@example.com"
}`}</pre>
            </div>

            <div className="param-details">
              <h4>Parameters:</h4>
              <table>
                <tbody>
                  <tr>
                    <td><code>github_url</code></td>
                    <td>string</td>
                    <td>required</td>
                    <td>Full GitHub repository URL (e.g., https://github.com/openai/openai-python)</td>
                  </tr>
                  <tr>
                    <td><code>email</code></td>
                    <td>string</td>
                    <td>required</td>
                    <td>Email address to share the documentation folder with (e.g., user@example.com)</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h4>Example Request:</h4>
            <div className="code-block">
              <pre>{`curl -X POST https://nyccode.org/api/v1/generate \\
  -H "Content-Type: application/json" \\
  -d '{
    "github_url": "https://github.com/openai/openai-python",
    "email": "user@example.com"
  }'`}</pre>
            </div>

            <h4>Response:</h4>
            <div className="code-block">
              <pre>{`{
  "success": true,
  "drive_link": "https://drive.google.com/drive/folders/1AbCdEfGhIjKlMnOpQrStUvWx",
  "folder_name": "psf_requests_20251009_143805",
  "ticket": "0",
  "status": "processing",
  "queue_position": 1,
  "estimated_time": "5-30 minutes"
}`}</pre>
            </div>

            <div className="response-note">
              <strong>💡 Tip:</strong> Save the <code>drive_link</code> immediately!
              It's available right away, even while documentation is still processing.
            </div>
          </div>

          <div className="endpoint">
            <h3><span className="method get">GET</span> /api/v1/status</h3>
            <p>Check the processing status of a documentation request</p>

            <h4>Query Parameters:</h4>
            <div className="param-details">
              <table>
                <tbody>
                  <tr>
                    <td><code>github_url</code></td>
                    <td>string</td>
                    <td>required</td>
                    <td>The same GitHub URL used in the generate request</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <h4>Example Request:</h4>
            <div className="code-block">
              <pre>{`curl "https://nyccode.org/api/v1/status?github_url=https://github.com/psf/requests"`}</pre>
            </div>

            <h4>Response (Processing):</h4>
            <div className="code-block">
              <pre>{`{
  "success": true,
  "status": "processing",
  "drive_link": "https://drive.google.com/drive/folders/1AbCdEfGhIjKlMnOpQrStUvWx",
  "folder_name": "psf_requests_20251009_143805"
}`}</pre>
            </div>

            <h4>Response (Completed):</h4>
            <div className="code-block">
              <pre>{`{
  "success": true,
  "status": "completed",
  "drive_link": "https://drive.google.com/drive/folders/1AbCdEfGhIjKlMnOpQrStUvWx",
  "master_doc_link": "https://docs.google.com/document/d/1XyZ123456789",
  "folder_name": "psf_requests_20251009_143805"
}`}</pre>
            </div>

            <div className="response-note">
              <strong>📊 Status Check:</strong> Poll this endpoint every 30-60 seconds to check progress.
              When status is <code>completed</code>, all documentation files are ready!
            </div>
          </div>
        </section>

        <section className="api-section">
          <h2>Status Values</h2>
          <ul className="status-list">
            <li><code>processing</code> - Documentation is being generated</li>
            <li><code>completed</code> - All files ready in Google Drive</li>
            <li><code>failed</code> - Processing failed (check error field)</li>
          </ul>
        </section>

        <section className="api-section">
          <h2>Code Examples</h2>

          <h3>Python</h3>
          <div className="code-block">
            <pre>{`import requests
import time

# Generate documentation
response = requests.post(
    'https://nyccode.org/api/v1/generate',
    json={
        'github_url': 'https://github.com/openai/openai-python',
        'email': 'user@example.com'
    }
)
result = response.json()
print(f"Drive Link: {result['drive_link']}")
print(f"Status: {result['status']}")

# Poll status
github_url = 'https://github.com/openai/openai-python'
while True:
    status = requests.get(
        'https://nyccode.org/api/v1/status',
        params={'github_url': github_url}
    ).json()

    if status['status'] == 'completed':
        print("Complete!")
        print(f"Master Doc: {status.get('master_doc_link', 'N/A')}")
        break

    time.sleep(30)  # Check every 30 seconds`}</pre>
          </div>

          <h3>JavaScript</h3>
          <div className="code-block">
            <pre>{`async function generateDocs() {
  const githubUrl = 'https://github.com/openai/openai-python';
  const email = 'user@example.com';

  // Generate documentation
  const response = await fetch('https://nyccode.org/api/v1/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      github_url: githubUrl,
      email: email
    })
  });

  const data = await response.json();
  console.log('Drive Link:', data.drive_link);
  console.log('Status:', data.status);

  // Poll status every 30 seconds
  const interval = setInterval(async () => {
    const status = await fetch(
      \`https://nyccode.org/api/v1/status?github_url=\${encodeURIComponent(githubUrl)}\`
    ).then(r => r.json());

    if (status.status === 'completed') {
      console.log('Complete!');
      console.log('Master Doc:', status.master_doc_link || 'N/A');
      clearInterval(interval);
    }
  }, 30000);
}

generateDocs();`}</pre>
          </div>
        </section>

        <section className="api-section">
          <h2>Best Practices</h2>
          <ul>
            <li><strong>Save the Drive link immediately</strong> - It's available instantly before processing completes</li>
            <li><strong>Poll status every 30-60 seconds</strong> - Don't poll too frequently</li>
            <li><strong>Handle long processing times</strong> - Large repositories may take 20-30 minutes</li>
            <li><strong>Cache results</strong> - Store drive links to avoid regenerating documentation</li>
          </ul>
        </section>

        <section className="api-section">
          <h2>Processing Timeline</h2>
          <div className="timeline">
            <div className="timeline-item">
              <strong>Instant (0s)</strong>
              <p>Drive folder created, link returned</p>
            </div>
            <div className="timeline-item">
              <strong>Processing (5-30min)</strong>
              <p>Documentation being generated</p>
            </div>
            <div className="timeline-item">
              <strong>Complete</strong>
              <p>All files available in Google Drive</p>
            </div>
          </div>
        </section>

        <section className="api-section api-specs">
          <h2>API Specifications</h2>
          <table>
            <tbody>
              <tr>
                <td><strong>Base URL</strong></td>
                <td>https://nyccode.org</td>
              </tr>
              <tr>
                <td><strong>Protocol</strong></td>
                <td>HTTPS</td>
              </tr>
              <tr>
                <td><strong>Authentication</strong></td>
                <td>None</td>
              </tr>
              <tr>
                <td><strong>Rate Limiting</strong></td>
                <td>None</td>
              </tr>
              <tr>
                <td><strong>CORS</strong></td>
                <td>Enabled</td>
              </tr>
            </tbody>
          </table>
        </section>
      </div>
    </div>
  );
}

export default ApiDocs;

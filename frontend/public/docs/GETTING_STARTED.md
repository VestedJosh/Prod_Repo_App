# Getting Started Guide

## What is NYC Code API?

NYC Code API transforms any public GitHub repository into comprehensive markdown documentation and delivers it instantly via Google Drive. No signup, no authentication, completely free.

---

## Quick Start (5 minutes)

### Step 1: Make Your First Request

```bash
curl -X POST https://nyccode.org/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"github_url": "https://github.com/psf/requests"}'
```

### Step 2: Get Your Drive Link

You'll receive an instant response:

```json
{
  "success": true,
  "drive_link": "https://drive.google.com/drive/folders/xxx",
  "ticket": "0",
  "status": "processing"
}
```

### Step 3: Access Your Documentation

1. **Immediately**: Click the `drive_link` to access your Google Drive folder
2. **Wait 5-30 minutes**: Documentation files are being generated
3. **Download**: All markdown files will appear in the folder

---

## Common Use Cases

### 1. Generate Documentation for Your Project

```python
my_repos = [
    'https://github.com/myorg/frontend',
    'https://github.com/myorg/backend',
    'https://github.com/myorg/mobile'
]

for repo in my_repos:
    result = generate_github_docs(repo)
    print(f"{repo} → {result['drive_link']}")
```

### 2. Share Documentation with Team

```python
def share_with_team(repo_url, team_emails):
    result = generate_github_docs(repo_url)

    for email in team_emails:
        send_email(
            to=email,
            subject=f"Documentation for {repo_url}",
            body=f"Access the docs here: {result['drive_link']}"
        )
```

### 3. Documentation Backup Service

```python
import schedule

def backup_docs():
    critical_repos = ['https://github.com/company/main-app']
    for repo in critical_repos:
        generate_github_docs(repo)

# Run weekly
schedule.every().monday.at("09:00").do(backup_docs)
```

---

## Troubleshooting

### "Invalid GitHub URL"
**Problem**: URL format is incorrect

**Solution**:
- Use format: `https://github.com/owner/repository`
- Don't use user profiles: `https://github.com/username` ✗
- Don't use organizations: `https://github.com/org` ✗

### Status Stuck on "processing"
**Problem**: Large repository taking longer than expected

**Solution**:
- Wait up to 30 minutes
- Check status every few minutes
- If still stuck after 30 min, try again

### "No processing found for this GitHub URL"
**Problem**: URL mismatch between generate and status calls

**Solution**:
- Use **exact same URL** for status checks
- URLs are case-sensitive
- Include/exclude `.git` consistently

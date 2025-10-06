# NYC Code - GCP Setup Guide (Production-Ready)

This guide documents the **exact steps** that successfully deployed NYC Code on Google Cloud Platform.

**Server Details:**
- Instance: `prod-repo-app-instance-v001`
- Zone: `us-east4-c`
- Project: `gen-lang-client-0933714587`
- External IP: `34.48.90.93`

---

## Prerequisites

- Google Cloud account with billing enabled
- GCP project created
- gcloud CLI installed and authenticated on local machine
- GitHub repository (can be private)
- Google OAuth credentials file (`client_secret_*.json`)

---

## Part 1: Connect to GCP Instance

### Step 1: Authenticate gcloud CLI (Local Machine)

```bash
# Install gcloud CLI first if not installed
# Windows: https://cloud.google.com/sdk/docs/install
# Mac: brew install google-cloud-sdk
# Linux: curl https://sdk.cloud.google.com | bash

# Authenticate
gcloud auth login

# Set project
gcloud config set project gen-lang-client-0933714587
```

### Step 2: SSH into Instance

```bash
gcloud compute ssh prod-repo-app-instance-v001 --zone us-east4-c
```

**Note:** If you get a host key prompt, type `y` to accept.

---

## Part 2: Install Docker & Docker Compose

Once connected to the GCP instance:

### Step 1: Update System

```bash
sudo apt-get update
```

### Step 2: Install Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### Step 3: Add User to Docker Group

```bash
sudo usermod -aG docker $USER
```

### Step 4: Apply Group Changes

**Option A:** Reconnect (Recommended)
```bash
exit
# Then reconnect:
gcloud compute ssh prod-repo-app-instance-v001 --zone us-east4-c
```

**Option B:** Use newgrp (May ask for password)
```bash
newgrp docker
```

### Step 5: Install Docker Compose

```bash
sudo apt-get install docker-compose-plugin -y
```

### Step 6: Verify Installation

```bash
docker --version
# Expected: Docker version 28.5.0+

docker compose version
# Expected: Docker Compose version v2.39.4+
```

---

## Part 3: Clone Repository

### Option 1: Public Repository

```bash
cd ~
git clone https://github.com/VestedJosh/Prod_Repo_App.git NYC_Code
cd NYC_Code
```

### Option 2: Private Repository

**Create GitHub Personal Access Token first:**
1. Go to https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scope: `repo` (full control)
4. Copy token (starts with `ghp_...`)

**Then clone:**
```bash
cd ~
git clone https://ghp_YOUR_TOKEN@github.com/VestedJosh/Prod_Repo_App.git NYC_Code
cd NYC_Code
```

---

## Part 4: Configure Environment

### Step 1: Create .env File

**Use vi editor (most reliable method):**

```bash
vi backend/.env
```

Press `i` to enter insert mode, then type these 3 lines:

```
FLASK_ENV=production
GOOGLE_CREDENTIALS_PATH=/app/client_secret_720052609656-btvogmsj00bk0e6eulc6ec412glnlr2i.apps.googleusercontent.com.json
TOKEN_DIR=/app/token-data
```

Press `Esc`, then type `:wq` and press `Enter` to save.

### Step 2: Verify .env File

```bash
cat backend/.env
```

**Expected output (3 clean lines, no breaks):**
```
FLASK_ENV=production
GOOGLE_CREDENTIALS_PATH=/app/client_secret_720052609656-btvogmsj00bk0e6eulc6ec412glnlr2i.apps.googleusercontent.com.json
TOKEN_DIR=/app/token-data
```

### Step 3: Get External IP (for Vercel)

```bash
curl ifconfig.me
echo ""
```

**Save this IP!** You'll need it for: `REACT_APP_API_URL=http://YOUR_IP:5000`

---

## Part 5: Build Docker Images

```bash
docker compose build
```

**Expected output:**
```
[+] Building 123.4s (XX/XX) FINISHED
=> [backend] ...
=> [frontend] ...
```

**Time:** 2-5 minutes depending on internet speed.

---

## Part 6: Deploy Services

### Step 1: Update Code from GitHub

```bash
cd ~/NYC_Code
git pull origin main
```

**Expected output:**
```
Updating 5f20012..41bb7e3
Fast-forward
 GCP_SETUP_GUIDE.md | 545 +++++++++++++++++++++
 backend/app.py     |   2 +-
 2 files changed, 546 insertions(+), 1 deletion(-)
```

### Step 2: Rebuild Backend Image

```bash
docker compose down
docker compose build backend
```

**Expected output:**
```
[+] Building 1.2s (14/14) FINISHED
```

### Step 3: Start All Services

```bash
docker compose up -d
```

### Step 4: Verify Services Are Running

```bash
docker compose ps
```

**Expected output:**
```
NAME                STATUS
nyc-code-backend    Up 8 seconds (healthy)
nyc-code-frontend   Up 8 seconds (health: starting)
```

---

## Part 7: Initial OAuth Authentication (If Needed)

**Note:** If you previously authenticated, the token already exists and you can skip this part.

### When OAuth Is Needed

If you see this error in logs:
```
Please visit this URL to authorize this application:
https://accounts.google.com/o/oauth2/auth?client_id=...
```

### Step 1: View Logs

```bash
docker compose logs backend
```

### Step 2: Copy OAuth URL

Find the line starting with:
```
Please visit this URL to authorize...
```

### Step 3: Authorize

1. Copy the entire URL
2. Open in your browser (on your local machine)
3. Sign in with your Google account
4. Grant all permissions (Drive, Sheets, Docs)
5. You'll see: "The authentication flow has completed"

### Step 4: Restart Services

```bash
docker compose restart backend
```

The token is now saved in the Docker volume.

---

## Part 8: Configure Firewall

### Allow Backend API Access on Port 5000

**On your local machine** (where gcloud CLI is installed):

```bash
gcloud compute firewall-rules create allow-backend-api --allow tcp:5000
```

**Expected output:**
```
Creating firewall...done.
NAME               NETWORK  DIRECTION  PRIORITY  ALLOW     DENY  DISABLED
allow-backend-api  default  INGRESS    1000      tcp:5000        False
```

**Optional:** Add more specific rules via GCP Console:

1. Go to **VPC network** → **Firewall**
2. Find `allow-backend-api`
3. Edit to add:
   - Description: "Allow backend API traffic"
   - Source IP ranges: Specific IPs instead of `0.0.0.0/0` for security

---

## Part 9: Test Backend

### Test 1: From GCP Instance (Internal)

**In your SSH session:**

```bash
curl http://localhost:5000/health
```

**Expected output:**
```json
{
  "message": "NYC Code API is running",
  "status": "ok"
}
```

### Test 2: From External (Your Local Machine)

**On your local machine:**

```bash
curl http://34.48.90.93:5000/health
```

**Or open in browser:**
```
http://34.48.90.93:5000/health
```

Should return the same JSON response.

**If external test fails:**
- Verify firewall rule exists: `gcloud compute firewall-rules list | grep allow-backend-api`
- Check backend is bound to 0.0.0.0: `docker compose logs backend | grep "Running on"`
- Should see: `Running on http://0.0.0.0:5000` (NOT `127.0.0.1`)

---

## Part 10: Connect Vercel Frontend

### Update Vercel Environment Variable

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Add/Update:
   - **Name:** `REACT_APP_API_URL`
   - **Value:** `http://34.48.90.93:5000`
   - **Environments:** Production, Preview, Development
5. Click **Save**
6. **Redeploy** your Vercel app

### Test Connection

Visit your Vercel site: https://www.nyccode.org

Open browser console and run:
```javascript
fetch('http://34.48.90.93:5000/health')
  .then(r => r.json())
  .then(console.log)
```

Should see: `{status: "ok", message: "NYC Code API is running"}`

---

## Useful Commands

### View Logs
```bash
docker compose logs -f backend        # Backend only
docker compose logs -f frontend       # Frontend only
docker compose logs -f                # All services
docker compose logs --tail=100        # Last 100 lines
```

### Restart Services
```bash
docker compose restart                # Restart all
docker compose restart backend        # Restart backend only
```

### Stop Services
```bash
docker compose down                   # Stop and remove containers
docker compose down -v                # Also remove volumes (WARNING: deletes token!)
```

### Update Application
```bash
cd ~/NYC_Code
git pull origin main
docker compose down
docker compose build
docker compose up -d
```

### Check Disk Usage
```bash
df -h                                 # Disk space
docker system df                      # Docker disk usage
docker system prune -a                # Clean up old images/containers
```

### Monitor Resources
```bash
docker stats                          # Real-time resource usage
htop                                  # System resources (install: sudo apt install htop)
```

---

## Troubleshooting

### Issue: Docker Permission Denied

**Solution:**
```bash
sudo usermod -aG docker $USER
exit
# Reconnect
gcloud compute ssh prod-repo-app-instance-v001 --zone us-east4-c
```

### Issue: Backend Won't Start

**Check logs:**
```bash
docker compose logs backend
```

**Common causes:**
- Missing credentials file
- Invalid .env file (check for line breaks)
- Token expired (delete volume and re-authenticate)

### Issue: Can't Access Backend Externally

**Check firewall:**
```bash
# On GCP instance
sudo ufw status

# Check GCP firewall rules
gcloud compute firewall-rules list | grep 5000
```

### Issue: OAuth Token Expired

**Delete token and re-authenticate:**
```bash
docker compose down
docker volume rm nyc_code_token-data
docker compose up backend
# Follow OAuth flow again
```

### Issue: Frontend Can't Connect

**Verify backend is accessible:**
```bash
curl http://34.48.90.93:5000/health
```

**Check CORS settings in `backend/app.py`:**
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://www.nyccode.org", "https://*.vercel.app"]
    }
})
```

---

## Security Best Practices

### 1. Restrict Firewall Access (Production)

Instead of `0.0.0.0/0`, limit to specific IPs:

```bash
gcloud compute firewall-rules update allow-backend-api \
  --source-ranges=YOUR_OFFICE_IP,VERCEL_IP_RANGES
```

### 2. Enable HTTPS

See `GCP_DEPLOYMENT.md` for SSL setup with Nginx and Certbot.

### 3. Regular Updates

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 4. Backup Token

```bash
docker run --rm -v nyc_code_token-data:/data -v ~/backups:/backup \
  ubuntu tar czf /backup/token-backup-$(date +%Y%m%d).tar.gz -C /data .
```

---

## Cost Management

### Current Setup Cost Estimate

- **GCP e2-medium instance:** ~$30/month
- **20 GB disk:** ~$1/month
- **Egress (to Google APIs):** Free
- **Static IP (if reserved):** $3/month (free if attached)

**Total:** ~$30-35/month

### Stop Instance to Save Costs

```bash
# From local machine
gcloud compute instances stop prod-repo-app-instance-v001 --zone us-east4-c
```

**Savings:** ~90% (only pay for disk storage)

### Start Instance

```bash
gcloud compute instances start prod-repo-app-instance-v001 --zone us-east4-c
```

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `gcloud compute ssh prod-repo-app-instance-v001 --zone us-east4-c` | Connect to instance |
| `cd ~/NYC_Code` | Go to project directory |
| `docker compose up -d` | Start services |
| `docker compose down` | Stop services |
| `docker compose logs -f` | View logs |
| `docker compose restart` | Restart services |
| `git pull origin main` | Update code |
| `curl http://localhost:5000/health` | Test backend |

---

## Success Checklist

- [x] Docker installed and working
- [x] Repository cloned
- [x] .env file configured (no line breaks!)
- [x] Docker images built successfully
- [x] OAuth authentication completed
- [x] Services running (`docker compose ps`)
- [x] Backend responding (`curl http://localhost:5000/health`)
- [x] Firewall rule created
- [x] External access working (`curl http://34.48.90.93:5000/health`)
- [x] Vercel environment variable updated
- [x] Frontend connecting to backend

---

## Support

- **GitHub Issues:** https://github.com/VestedJosh/Prod_Repo_App/issues
- **GCP Documentation:** https://cloud.google.com/docs
- **Docker Documentation:** https://docs.docker.com/

---

**Congratulations! Your NYC Code backend is now live on GCP!** 🎉

Frontend: https://www.nyccode.org
Backend: http://34.48.90.93:5000

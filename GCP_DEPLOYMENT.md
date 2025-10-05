# NYC Code - Complete GCP Deployment Guide

This comprehensive guide will walk you through deploying the NYC Code documentation generator on Google Cloud Platform (GCP).

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [GCP Account Setup](#gcp-account-setup)
3. [Create GCP Compute Instance](#create-gcp-compute-instance)
4. [Initial Server Setup](#initial-server-setup)
5. [Install Docker & Docker Compose](#install-docker--docker-compose)
6. [Google API Setup](#google-api-setup)
7. [Deploy Application](#deploy-application)
8. [Configure Domain & SSL (Optional)](#configure-domain--ssl-optional)
9. [Monitoring & Maintenance](#monitoring--maintenance)
10. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:
- Google Account
- Credit card for GCP (new users get $300 free credit)
- SSH client (Terminal on Mac/Linux, PuTTY on Windows)
- Basic command line knowledge

---

## GCP Account Setup

### 1. Create GCP Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Accept terms and activate free trial ($300 credit, 90 days)
4. Enter billing information (won't be charged during trial)

### 2. Create New Project

1. Click **Select a project** → **New Project**
2. Project name: `nyc-code-production`
3. Click **Create**
4. Wait for project creation (takes ~30 seconds)

### 3. Enable Required APIs

```bash
# In Cloud Console, open Cloud Shell (top right icon)
gcloud services enable compute.googleapis.com
gcloud services enable drive.googleapis.com
gcloud services enable sheets.googleapis.com
gcloud services enable docs.googleapis.com
```

---

## Create GCP Compute Instance

### Option A: Using Cloud Console (Recommended for Beginners)

1. **Navigate to Compute Engine**
   - Left menu → Compute Engine → VM instances
   - Click **Create Instance**

2. **Configure Instance**
   - **Name:** `nyc-code-server`
   - **Region:** `us-central1` (Iowa)
   - **Zone:** `us-central1-a`

3. **Machine Configuration**
   - **Series:** E2
   - **Machine type:** `e2-small` (2 vCPU, 2 GB memory) - ~$15/month
   - For heavier usage, choose `e2-medium` (2 vCPU, 4 GB memory) - ~$30/month

4. **Boot Disk**
   - Click **Change**
   - **Operating system:** Ubuntu
   - **Version:** Ubuntu 22.04 LTS
   - **Boot disk type:** Standard persistent disk
   - **Size:** 20 GB
   - Click **Select**

5. **Firewall**
   - ✅ Allow HTTP traffic
   - ✅ Allow HTTPS traffic

6. **Advanced Options → Networking**
   - **Network tags:** Add `http-server`, `https-server`

7. Click **Create** and wait ~30 seconds

### Option B: Using gcloud CLI (For Advanced Users)

```bash
gcloud compute instances create nyc-code-server \
  --project=nyc-code-production \
  --zone=us-central1-a \
  --machine-type=e2-small \
  --image-family=ubuntu-2204-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=20GB \
  --boot-disk-type=pd-standard \
  --tags=http-server,https-server \
  --metadata=startup-script='#!/bin/bash
    apt-get update
    apt-get install -y docker.io docker-compose git curl
    systemctl enable docker
    systemctl start docker
  '
```

### 3. Configure Firewall Rules

```bash
# Allow HTTP traffic (port 80)
gcloud compute firewall-rules create allow-http \
  --allow tcp:80 \
  --target-tags http-server \
  --description="Allow HTTP traffic" \
  --direction=INGRESS

# Allow HTTPS traffic (port 443)
gcloud compute firewall-rules create allow-https \
  --allow tcp:443 \
  --target-tags https-server \
  --description="Allow HTTPS traffic" \
  --direction=INGRESS

# Allow backend port (5000) - optional, for debugging
gcloud compute firewall-rules create allow-backend \
  --allow tcp:5000 \
  --target-tags http-server \
  --description="Allow backend API traffic" \
  --direction=INGRESS
```

### 4. Reserve Static IP Address (Recommended)

```bash
# Reserve external IP
gcloud compute addresses create nyc-code-ip \
  --region=us-central1

# Get the IP address
gcloud compute addresses describe nyc-code-ip \
  --region=us-central1 \
  --format="get(address)"

# Assign to instance
gcloud compute instances delete-access-config nyc-code-server \
  --zone=us-central1-a \
  --access-config-name="external-nat"

gcloud compute instances add-access-config nyc-code-server \
  --zone=us-central1-a \
  --access-config-name="external-nat" \
  --address=nyc-code-ip
```

---

## Initial Server Setup

### 1. Connect to Server

**Using Cloud Console (Easiest):**
1. Go to Compute Engine → VM instances
2. Click **SSH** button next to your instance

**Using gcloud CLI:**
```bash
gcloud compute ssh nyc-code-server --zone=us-central1-a
```

**Using Standard SSH:**
```bash
# Get external IP from Cloud Console
ssh -i ~/.ssh/google_compute_engine your-username@EXTERNAL_IP
```

### 2. Update System Packages

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 3. Create Application User (Security Best Practice)

```bash
# Create user
sudo useradd -m -s /bin/bash nyccode
sudo usermod -aG sudo nyccode

# Set password
sudo passwd nyccode

# Switch to new user
sudo su - nyccode
```

---

## Install Docker & Docker Compose

### 1. Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add current user to docker group (avoid using sudo)
sudo usermod -aG docker $USER

# Apply group changes
newgrp docker

# Verify installation
docker --version
```

### 2. Install Docker Compose

```bash
# Install Docker Compose
sudo apt-get install docker-compose-plugin -y

# Verify installation
docker compose version
```

### 3. Enable Docker to Start on Boot

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

---

## Google API Setup

### 1. Create OAuth 2.0 Credentials

1. **Go to Google Cloud Console**
   - Navigate to [APIs & Services → Credentials](https://console.cloud.google.com/apis/credentials)

2. **Configure OAuth Consent Screen**
   - Click **OAuth consent screen**
   - User Type: **External**
   - Click **Create**
   - Fill in required fields:
     - App name: `NYC Code Documentation Generator`
     - User support email: Your email
     - Developer contact: Your email
   - Click **Save and Continue**
   - Scopes: Click **Add or Remove Scopes**
     - Select: `Google Drive API` (all scopes)
     - Select: `Google Sheets API` (all scopes)
     - Select: `Google Docs API` (all scopes)
   - Click **Save and Continue**
   - Test users: Add your email
   - Click **Save and Continue**

3. **Create OAuth Client ID**
   - Click **Credentials** → **Create Credentials** → **OAuth client ID**
   - Application type: **Desktop app**
   - Name: `NYC Code Backend`
   - Click **Create**
   - Download JSON file → rename to `client_secret.json`

### 2. Enable Required APIs

```bash
# In Cloud Shell or your terminal
gcloud services enable drive.googleapis.com
gcloud services enable sheets.googleapis.com
gcloud services enable docs.googleapis.com
```

---

## Deploy Application

### 1. Clone Repository

```bash
# SSH into your server first
cd ~
git clone https://github.com/YOUR_USERNAME/NYC_Code.git
cd NYC_Code
```

**OR** if you don't have a Git repo, upload files manually:

```bash
# On your local machine, create a tarball
cd /path/to/NYC_Code
tar -czf nyc-code.tar.gz backend/ frontend/ docker-compose.yml

# Upload to server (from your local machine)
gcloud compute scp nyc-code.tar.gz nyc-code-server:~ --zone=us-central1-a

# On server, extract
cd ~
tar -xzf nyc-code.tar.gz
```

### 2. Upload Google Credentials

```bash
# From your local machine
gcloud compute scp /path/to/client_secret_*.json \
  nyc-code-server:~/NYC_Code/backend/ \
  --zone=us-central1-a
```

### 3. Create Environment File

```bash
# On server
cd ~/NYC_Code/backend
nano .env
```

Add the following:
```env
FLASK_ENV=production
GOOGLE_CREDENTIALS_PATH=/app/client_secret_720052609656-btvogmsj00bk0e6eulc6ec412glnlr2i.apps.googleusercontent.com.json
TOKEN_DIR=/app/token-data
```

Save and exit (Ctrl+X, Y, Enter)

### 4. Update Frontend API URL

```bash
# Edit frontend environment
cd ~/NYC_Code/frontend
nano .env.production
```

Add:
```env
REACT_APP_API_URL=http://YOUR_EXTERNAL_IP:5000
```

**Replace `YOUR_EXTERNAL_IP` with your server's external IP**

Get external IP:
```bash
curl ifconfig.me
```

### 5. Build Docker Images

```bash
cd ~/NYC_Code

# Build images
docker compose build

# This takes 5-10 minutes
```

### 6. Start Services (Initial Auth Required)

**Important: First run requires OAuth authentication**

```bash
# Start backend only for initial authentication
docker compose up backend
```

You'll see output like:
```
Please visit this URL to authorize this application:
https://accounts.google.com/o/oauth2/auth?client_id=...
```

**On your local machine:**
1. Copy the URL from server output
2. Open in browser
3. Sign in with Google account
4. Grant all permissions
5. You'll see "The authentication flow has completed"

**Back on server:**
- Press Ctrl+C to stop
- Token is now saved in volume

### 7. Start All Services

```bash
# Start in detached mode
docker compose up -d

# Check logs
docker compose logs -f

# Verify services are running
docker compose ps
```

### 8. Test the Application

```bash
# Test backend
curl http://localhost:5000/health

# Test from outside
curl http://YOUR_EXTERNAL_IP/health
```

Open browser: `http://YOUR_EXTERNAL_IP`

---

## Configure Domain & SSL (Optional)

### 1. Point Domain to Server

1. Buy domain from [Google Domains](https://domains.google.com/), [Namecheap](https://www.namecheap.com/), etc.
2. Add DNS A record:
   - Type: `A`
   - Name: `@` (or `www`)
   - Value: `YOUR_EXTERNAL_IP`
   - TTL: `3600`

Wait 5-60 minutes for DNS propagation

### 2. Install Certbot for SSL

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Follow prompts:
# - Enter email
# - Agree to terms
# - Redirect HTTP to HTTPS: Yes
```

### 3. Update Docker Compose for SSL

Edit `docker-compose.yml`:
```yaml
frontend:
  ports:
    - "80:80"
    - "443:443"  # Add this
  volumes:
    - /etc/letsencrypt:/etc/letsencrypt:ro  # Add this
```

Restart:
```bash
docker compose down
docker compose up -d
```

---

## Monitoring & Maintenance

### 1. View Logs

```bash
# All services
docker compose logs -f

# Backend only
docker compose logs -f backend

# Frontend only
docker compose logs -f frontend

# Last 100 lines
docker compose logs --tail=100
```

### 2. Check Service Status

```bash
# Container status
docker compose ps

# Resource usage
docker stats

# Disk usage
df -h
docker system df
```

### 3. Restart Services

```bash
# Restart all
docker compose restart

# Restart backend only
docker compose restart backend

# Rebuild and restart
docker compose up -d --build
```

### 4. Update Application

```bash
# Pull latest code
cd ~/NYC_Code
git pull

# Rebuild and restart
docker compose down
docker compose build
docker compose up -d
```

### 5. Backup Token and Data

```bash
# Create backup directory
mkdir -p ~/backups

# Backup token
docker run --rm -v nyc_code_token-data:/data -v ~/backups:/backup \
  ubuntu tar czf /backup/token-backup-$(date +%Y%m%d).tar.gz -C /data .

# Backup data directory
tar czf ~/backups/data-backup-$(date +%Y%m%d).tar.gz backend/data/

# Download backups to local machine
gcloud compute scp nyc-code-server:~/backups/* ./backups/ \
  --zone=us-central1-a --recurse
```

### 6. Set Up Automatic Backups (Cron)

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * cd ~/NYC_Code && docker run --rm -v nyc_code_token-data:/data -v ~/backups:/backup ubuntu tar czf /backup/token-backup-$(date +\%Y\%m\%d).tar.gz -C /data .
```

### 7. Monitor Google Sheet

Access tracking sheet:
1. Go to your Google Drive
2. Find folder: `NYC_Code_Backend`
3. Open: `NYC_Code_Tracking` spreadsheet
4. Monitor queue status (Processing/Complete)

---

## Troubleshooting

### Backend Won't Start

```bash
# Check logs
docker compose logs backend

# Common issues:
# 1. Missing credentials
ls backend/client_secret_*.json

# 2. Token issues
docker compose exec backend ls -la /app/token-data/

# 3. Port conflict
sudo lsof -i :5000
```

### Frontend Can't Reach Backend

```bash
# Check frontend API URL
docker compose exec frontend cat /usr/share/nginx/html/static/js/*.js | grep -o 'http://[^"]*'

# Test backend from frontend container
docker compose exec frontend wget -O- http://backend:5000/health

# Check firewall
sudo ufw status
gcloud compute firewall-rules list
```

### OAuth Token Expired

```bash
# Delete token and re-authenticate
docker compose down
docker volume rm nyc_code_token-data
docker compose up backend

# Follow OAuth flow again (see step 6 in Deploy Application)
```

### Out of Memory

```bash
# Check memory usage
free -h
docker stats

# Solution: Upgrade to e2-medium
gcloud compute instances stop nyc-code-server --zone=us-central1-a
gcloud compute instances set-machine-type nyc-code-server \
  --machine-type=e2-medium \
  --zone=us-central1-a
gcloud compute instances start nyc-code-server --zone=us-central1-a
```

### Google Drive Upload Fails

```bash
# Check credentials
docker compose exec backend python -c "from services.google_drive import test_connection; print(test_connection())"

# Re-authenticate
docker compose down
docker volume rm nyc_code_token-data
docker compose up backend
# Follow OAuth flow
```

### Queue Not Processing

```bash
# Check queue status
curl http://localhost:5000/api/queue-status

# Check backend logs
docker compose logs -f backend | grep Queue

# Restart backend
docker compose restart backend
```

### Disk Full

```bash
# Check disk usage
df -h

# Clean up Docker
docker system prune -a --volumes

# Clean up old data
cd ~/NYC_Code/backend
rm -rf output/*.md data/*.csv
```

---

## Cost Optimization

### 1. Stop Instance When Not in Use

```bash
# Stop instance (preserves disk)
gcloud compute instances stop nyc-code-server --zone=us-central1-a

# Start instance
gcloud compute instances start nyc-code-server --zone=us-central1-a
```

### 2. Schedule Auto-Shutdown

```bash
# Add to crontab (shutdown at midnight)
crontab -e

# Add line:
0 0 * * * gcloud compute instances stop nyc-code-server --zone=us-central1-a
```

### 3. Downgrade Instance Type

If traffic is low:
```bash
# Change to e2-micro (1 vCPU, 1 GB) - ~$7/month
gcloud compute instances set-machine-type nyc-code-server \
  --machine-type=e2-micro \
  --zone=us-central1-a
```

---

## Security Best Practices

### 1. Enable Firewall

```bash
# Enable UFW
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. Automatic Security Updates

```bash
sudo apt-get install unattended-upgrades -y
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

### 3. Limit SSH Access

```bash
# Edit SSH config
sudo nano /etc/ssh/sshd_config

# Change:
PermitRootLogin no
PasswordAuthentication no

# Restart SSH
sudo systemctl restart sshd
```

### 4. Set Up Monitoring Alerts

```bash
# Install monitoring agent
curl -sSO https://dl.google.com/cloudagents/add-monitoring-agent-repo.sh
sudo bash add-monitoring-agent-repo.sh
sudo apt-get update
sudo apt-get install stackdriver-agent -y
sudo service stackdriver-agent start
```

---

## Quick Reference Commands

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f

# Restart services
docker compose restart

# Check status
docker compose ps

# Update application
git pull && docker compose up -d --build

# Backup token
docker run --rm -v nyc_code_token-data:/data -v ~/backups:/backup ubuntu tar czf /backup/token.tar.gz -C /data .

# Access shell in backend
docker compose exec backend bash

# Check queue status
curl http://localhost:5000/api/queue-status
```

---

## Support & Additional Resources

- **GCP Documentation:** https://cloud.google.com/docs
- **Docker Documentation:** https://docs.docker.com/
- **Google Drive API:** https://developers.google.com/drive
- **Issue Tracker:** [Your GitHub Issues URL]

---

## Estimated Monthly Costs

| Instance Type | vCPU | RAM | Cost/Month | Repos/Day |
|---------------|------|-----|------------|-----------|
| e2-micro | 2 | 1 GB | $7 | 1-10 |
| e2-small | 2 | 2 GB | $15 | 10-50 |
| e2-medium | 2 | 4 GB | $30 | 50-200 |

**Additional costs:**
- Static IP: $3/month (if not attached to running instance)
- Egress traffic: Usually free for Google API calls
- Storage: 20 GB = ~$0.80/month

**Total estimated cost:** $15-35/month for most use cases

---

## Congratulations! 🎉

Your NYC Code documentation generator is now running on GCP!

Access your app at: `http://YOUR_EXTERNAL_IP`

Or with domain: `https://yourdomain.com`

# 🔒 SECURITY TODO - URGENT

## ⚠️ Google OAuth Credentials Compromised

**Date Identified:** October 6, 2025

### Issue
The `client_secret` file was accidentally committed to git repository and needs to be rotated.

**Exposed Credentials:**
- **Project ID:** `gen-lang-client-0933714587`
- **Client ID:** `720052609656-btvogmsj00bk0e6eulc6ec412glnlr2i.apps.googleusercontent.com`
- **Client Secret:** `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`

### Action Required

1. **Revoke Old Credentials**
   - Go to: https://console.cloud.google.com/apis/credentials?project=gen-lang-client-0933714587
   - Find OAuth 2.0 Client ID: `720052609656-btvogmsj00bk0e6eulc6ec412glnlr2i`
   - Click "Delete" to revoke

2. **Create New Credentials**
   - In same console, click "Create Credentials" > "OAuth 2.0 Client ID"
   - Application type: "Desktop app"
   - Name: "NYC Code Backend"
   - Download the new `client_secret_*.json` file

3. **Update Backend**
   - Replace old `client_secret_*.json` in `backend/` folder
   - Delete `token.pickle` (if exists)
   - Restart backend app to re-authenticate

4. **Verify .gitignore**
   - ✅ Already updated to use wildcard patterns
   - ✅ Old credentials removed from git tracking

5. **(Optional) Clean Git History**
   - If repo is public or widely shared, consider using:
     - BFG Repo-Cleaner: https://rtyley.github.io/bfg-repo-cleaner/
     - Git filter-branch
   - This removes the secret from all historical commits

### Risk Level
🟡 **Medium** - Can cause quota abuse and reputation damage, but cannot directly access user data.

### Status
- [ ] Credentials revoked in Google Cloud Console
- [ ] New credentials generated
- [ ] Backend updated with new credentials
- [ ] Backend re-authenticated successfully
- [ ] Old credentials confirmed non-functional

---
**Remember:** Never commit files matching these patterns:
- `client_secret*.json`
- `credentials*.json`
- `token*.json` / `*.pickle`
- `.env`

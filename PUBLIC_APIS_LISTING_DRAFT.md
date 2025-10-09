# NYC Code API - Public APIs Listing Draft

## Repository
https://github.com/public-apis/public-apis

---

## API Entry

### Category: **Development**
(Alternative category: Documentation)

### Table Entry
```markdown
| [NYC Code](https://nyccode.org) | Generate markdown documentation for any public GitHub repository | No | Yes | Yes | No |
```

### Field Breakdown
- **API Name**: NYC Code
  - ✅ No "API" suffix
  - ✅ No TLD (.org)
  - ✅ Links to https://nyccode.org (main site with API docs)

- **Description**: "Generate markdown documentation for any public GitHub repository"
  - ✅ 69 characters (under 100 character limit)
  - ✅ Clear and descriptive
  - ✅ Explains what the API does

- **Auth**: No
  - ✅ No authentication required to use the API

- **HTTPS**: Yes
  - ✅ API uses HTTPS protocol

- **CORS**: Yes
  - ✅ CORS is enabled for all origins

- **Call this API**: No
  - No Postman collection available yet

---

## Pull Request Details

### PR Title
```
Add NYC Code API
```

### Commit Message
```
Add NYC Code API to Development
```

### PR Description Template
```markdown
## Description
Adding NYC Code API to the Development category.

## API Details
- **Name**: NYC Code
- **URL**: https://nyccode.org
- **Category**: Development
- **Free**: Yes (100% free, no paid tiers)
- **Authentication**: None required
- **CORS**: Enabled
- **Documentation**: Available at https://nyccode.org (click "API Docs" button)

## API Purpose
NYC Code generates comprehensive markdown documentation for any public GitHub repository. Users provide a GitHub URL and email, and receive a Google Drive folder with complete documentation files.

## Checklist
- [x] API has full, free access
- [x] No device/service purchase required
- [x] Proper documentation available
- [x] Description under 100 characters
- [x] Alphabetical ordering maintained
- [x] No "API" suffix in name
- [x] No TLD in name
- [x] HTTPS supported
- [x] CORS enabled
```

---

## Submission Steps

### 1. Fork the Repository
```bash
# Go to https://github.com/public-apis/public-apis
# Click "Fork" button
```

### 2. Clone Your Fork
```bash
git clone https://github.com/YOUR_USERNAME/public-apis.git
cd public-apis
```

### 3. Create a Branch
```bash
git checkout -b add-nyc-code-api
```

### 4. Find the Development Section
Edit the `README.md` file and locate the "Development" section.
Insert the entry in alphabetical order (NYC Code comes after "Netlify" and before "Ory").

### 5. Add the Entry
```markdown
### Development
API | Description | Auth | HTTPS | CORS | Call this API
|---|---|---|---|---|---|
| [Netlify](https://docs.netlify.com/api/get-started/) | Netlify is a hosting service for the programmable web | `OAuth` | Yes | Unknown | No |
| [NYC Code](https://nyccode.org) | Generate markdown documentation for any public GitHub repository | No | Yes | Yes | No |
| [Ory](https://www.ory.sh/docs/ecosystem/api-design) | Authentication, authorization, access control and delegation of authorization | `apiKey` | Yes | Yes | No |
```

### 6. Commit Your Changes
```bash
git add README.md
git commit -m "Add NYC Code API to Development"
```

### 7. Push to Your Fork
```bash
git push origin add-nyc-code-api
```

### 8. Create Pull Request
1. Go to your fork on GitHub
2. Click "Compare & pull request"
3. Title: `Add NYC Code API`
4. Use the PR description template above
5. Submit the pull request to the `master` branch

---

## Alternative Descriptions (if 69 chars is too long)

1. "Generate markdown docs for any public GitHub repository" (61 chars)
2. "Auto-generate documentation for GitHub repositories" (51 chars)
3. "Create markdown documentation from GitHub repos" (47 chars)
4. "Generate GitHub repository documentation" (40 chars)

---

## Key Points for Review

### ✅ Meets Requirements
- **Free Access**: 100% free, no paid tiers or limitations
- **No Purchase Required**: Doesn't require any device or service purchase
- **Proper Documentation**: Comprehensive API docs available at https://nyccode.org
- **CORS Enabled**: API supports CORS for client-side usage
- **HTTPS**: Secure HTTPS protocol
- **No Auth Required**: Simple to use, no API keys needed

### 📝 API Endpoints
- `POST /api/v1/generate` - Generate documentation
- `GET /api/v1/status` - Check processing status

### 🎯 Target Audience
Developers who want to:
- Generate documentation for open source projects
- Create comprehensive code documentation automatically
- Document GitHub repositories in markdown format

---

## Expected Questions & Answers

**Q: Is this free?**
A: Yes, 100% free with no limits or paid tiers.

**Q: Does it require authentication?**
A: No, the API is public and requires no authentication.

**Q: Is the source code available?**
A: The API is currently closed source, but the frontend is open source.

**Q: What makes this different from other documentation tools?**
A: NYC Code automatically generates comprehensive markdown documentation directly from GitHub repositories and delivers them via Google Drive.

**Q: Is this a marketing attempt?**
A: No, this is a genuinely free developer tool with no paid services or upsells.

---

## Notes

- Ensure the build passes after submitting the PR
- Be ready to squash commits if changes are requested
- Monitor the PR for any feedback from maintainers
- The API documentation is accessible via the "API Docs" button on https://nyccode.org

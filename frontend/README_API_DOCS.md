# NYC Code Frontend - API Documentation

## New Files Added

The following files have been added to document the NYC Code API:

### 1. Documentation Files (in `public/docs/`)
- `API_DOCUMENTATION.md` - Complete API reference
- `GETTING_STARTED.md` - Quick start guide
- `INTEGRATION_GUIDE.md` - Integration patterns and examples

### 2. API Documentation Component
- `src/components/ApiDocs.js` - React component displaying API documentation
- `src/components/ApiDocs.css` - Styling for the API docs component

---

## How to Use the API Documentation Component

### Option 1: Add as a separate page/route

If you have React Router installed:

```javascript
// In your App.js or main routing file
import ApiDocs from './components/ApiDocs';

// Add route
<Route path="/api-docs" element={<ApiDocs />} />
```

### Option 2: Add a link in your main app

```javascript
// In App.js
<a href="/api-docs" target="_blank">View API Documentation</a>
```

### Option 3: Display inline

```javascript
// In App.js, add at the bottom
import ApiDocs from './components/ApiDocs';

// In your JSX
<div>
  {/* Your existing UI */}
  <ApiDocs />
</div>
```

---

## Testing Locally

```bash
cd frontend
npm start
```

Then visit:
- Main app: http://localhost:3000
- API docs (if routed): http://localhost:3000/api-docs

---

## API Endpoints Summary

### Generate Documentation
```bash
POST https://nyccode.org/api/v1/generate
Body: { "github_url": "https://github.com/owner/repo" }
```

### Check Status
```bash
GET https://nyccode.org/api/v1/status?github_url=<url>
```

---

## Key Changes from Session Context

- All backend processing (queueing, processing, uploading) is referred to as "processing"
- Status values simplified: `processing`, `completed`, `failed`
- No mention of internal backend operations
- Focus on user-facing features: Drive link, status updates, estimated time

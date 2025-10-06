# NYC Code - Backend (Python/Flask)

Python Flask backend for generating GitHub repository documentation using DeepWiki scraping.

## Features

- Converts GitHub URLs to DeepWiki URLs
- Scrapes DeepWiki for documentation (with mock fallback for testing)
- Saves documentation as Markdown files
- Stores submission data in CSV (simulates Google Sheets)
- CORS enabled for frontend integration

## Setup

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python app.py
```

The server will start at `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /health
```

### Generate Documentation
```
POST /api/generate-docs
Body: { "githubUrl": "https://github.com/openai/openai-python" }
```

### Share Documentation
```
POST /api/share-docs
Body: {
  "githubUrl": "https://github.com/openai/openai-python",
  "email": "user@example.com"
}
```

## Project Structure

```
backend/
├── app.py                          # Flask server
├── requirements.txt                # Dependencies
├── services/
│   ├── __init__.py
│   ├── doc_generator.py           # DeepWiki scraper & URL converter
│   └── storage.py                 # CSV & Markdown storage
├── data/
│   └── submissions.csv            # User submissions (auto-created)
└── output/
    └── *.md                       # Generated markdown files
```

## How It Works

1. **GitHub → DeepWiki**: Converts `github.com/owner/repo` to `deepwiki.com/owner/repo`
2. **Scraping**: Scrapes DeepWiki page and converts to Markdown
3. **Storage**: Saves markdown to `output/` folder
4. **CSV Logging**: Logs email, repo, and timestamp to `data/submissions.csv`

## Testing Locally

The backend uses mock documentation generation for testing when DeepWiki is unavailable. All data is stored locally in CSV and Markdown files.

## Dependencies

- Flask: Web framework
- flask-cors: CORS support
- requests: HTTP client
- beautifulsoup4: HTML parsing
- python-dotenv: Environment variables

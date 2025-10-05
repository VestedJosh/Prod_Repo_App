# NYC Code - Frontend

React-based frontend for generating GitHub repository documentation and sharing it via Google Drive.

## Features

- **Step 1**: Enter a public GitHub repository URL
- **Step 2**: Generate documentation automatically
- **Step 3**: Share documentation to Google Drive via email

## Setup

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file from the example:
```bash
cp .env.example .env
```

3. Update the `.env` file with your backend API URL:
```
REACT_APP_API_URL=http://localhost:5000
```

### Running the Application

Start the development server:
```bash
npm start
```

The app will open at [http://localhost:3000](http://localhost:3000)

### Build for Production

```bash
npm run build
```

## Project Structure

```
frontend/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── App.js              # Main application component
│   ├── App.css             # Application styles
│   ├── index.js            # Entry point
│   └── index.css           # Global styles
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── package.json            # Dependencies
└── README.md               # This file
```

## How It Works

1. **GitHub URL Input**: User enters a GitHub repository URL (e.g., `https://github.com/openai/openai-python`)

2. **Documentation Generation**: The backend converts the GitHub URL to DeepWiki format and scrapes the documentation

3. **Email Submission**: User enters their email to receive the documentation

4. **Google Drive Sharing**: Documentation is uploaded to Google Drive and shared with the user's email

## Environment Variables

- `REACT_APP_API_URL`: Backend API URL (default: `http://localhost:5000`)

## Dependencies

- **react**: UI library
- **react-dom**: React DOM rendering
- **axios**: HTTP client for API calls
- **react-scripts**: Create React App scripts

## License

MIT

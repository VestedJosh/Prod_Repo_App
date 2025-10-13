import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import confetti from 'canvas-confetti';
import ApiDocs from './components/ApiDocs';
import './App.css';

function App() {
  const [showApiDocs, setShowApiDocs] = useState(false);
  const [step, setStep] = useState(1);
  const [githubUrl, setGithubUrl] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [driveLink, setDriveLink] = useState('');
  const [folderName, setFolderName] = useState('');
  const [ticket, setTicket] = useState('');
  const [status, setStatus] = useState('');
  const [queuePosition, setQueuePosition] = useState(null);
  const [estimatedTime, setEstimatedTime] = useState('');
  const [masterDocLink, setMasterDocLink] = useState('');
  const pollingInterval = useRef(null);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  // Status polling effect
  useEffect(() => {
    if (step === 2 && githubUrl) {
      // Start polling for status updates
      pollingInterval.current = setInterval(async () => {
        try {
          const response = await axios.get(`${API_BASE_URL}/api/v1/status`, {
            params: { github_url: githubUrl }
          });

          if (response.data.success) {
            const newStatus = response.data.status;
            setStatus(newStatus);

            if (response.data.master_doc_link) {
              setMasterDocLink(response.data.master_doc_link);
            }

            // If completed or failed, stop polling and move to final step
            if (newStatus === 'completed') {
              clearInterval(pollingInterval.current);
              setMessage('Documentation complete!');

              // Trigger confetti animation
              const duration = 2000;
              const animationEnd = Date.now() + duration;
              const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

              function randomInRange(min, max) {
                return Math.random() * (max - min) + min;
              }

              const interval = setInterval(function() {
                const timeLeft = animationEnd - Date.now();

                if (timeLeft <= 0) {
                  return clearInterval(interval);
                }

                const particleCount = 50 * (timeLeft / duration);

                confetti(Object.assign({}, defaults, {
                  particleCount,
                  origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 }
                }));
                confetti(Object.assign({}, defaults, {
                  particleCount,
                  origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 }
                }));
              }, 250);

              setStep(3);
            } else if (newStatus === 'failed') {
              clearInterval(pollingInterval.current);
              setError(response.data.error || 'Documentation generation failed');
            }
          }
        } catch (err) {
          console.error('Status polling error:', err);
        }
      }, 30000); // Poll every 30 seconds

      // Cleanup on unmount
      return () => {
        if (pollingInterval.current) {
          clearInterval(pollingInterval.current);
        }
      };
    }
  }, [step, githubUrl, API_BASE_URL]);

  const handleGenerateDocs = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setMessage('');

    try {
      const response = await axios.post(`${API_BASE_URL}/api/v1/generate`, {
        github_url: githubUrl,
        email: email
      });

      if (response.data.success) {
        setDriveLink(response.data.drive_link);
        setFolderName(response.data.folder_name);
        setTicket(response.data.ticket);
        setStatus(response.data.status);
        setQueuePosition(response.data.queue_position);
        setEstimatedTime(response.data.estimated_time);
        setMessage('Documentation generation started! Your Drive folder is ready.');
        setStep(2); // Move to processing step
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to generate documentation');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setStep(1);
    setGithubUrl('');
    setEmail('');
    setMessage('');
    setError('');
    setDriveLink('');
    setFolderName('');
    setTicket('');
    setStatus('');
    setQueuePosition(null);
    setEstimatedTime('');
    setMasterDocLink('');
    if (pollingInterval.current) {
      clearInterval(pollingInterval.current);
    }
  };

  // If showing API docs, render that component
  if (showApiDocs) {
    return (
      <div className="App">
        <div className="nav-header">
          <button
            className="nav-button"
            onClick={() => setShowApiDocs(false)}
          >
            ← Back to Home
          </button>
        </div>
        <ApiDocs />
      </div>
    );
  }

  return (
    <div className="App">
      <div className="container">
        <h1>NYC Code</h1>
        <p className="subtitle">Generate Documentation for GitHub Repositories</p>

        {step === 1 && (
          <div className="step-container">
            <h2>Generate GitHub Documentation</h2>
            <form onSubmit={handleGenerateDocs}>
              <input
                type="url"
                className="input-field"
                placeholder="GitHub URL: https://github.com/openai/openai-python"
                value={githubUrl}
                onChange={(e) => setGithubUrl(e.target.value)}
                required
              />
              <input
                type="email"
                className="input-field"
                placeholder="Email: your.email@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? 'Starting...' : 'Generate Documentation'}
              </button>
            </form>
            <p className="info-text">
              Documentation will be generated and shared to your Google Drive. Processing takes 5-30 minutes depending on repository size.
            </p>
          </div>
        )}

        {step === 2 && (
          <div className="step-container">
            <h2>Processing Your Documentation...</h2>
            <div className="timer-container">
              <div className="spinner"></div>
              <p className="timer-text">
                Your documentation folder has been created and is being populated with content.
              </p>

              {driveLink && (
                <div className="drive-link-box">
                  <p><strong>Your Drive folder is ready:</strong></p>
                  <a
                    href={driveLink}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="drive-link"
                  >
                    Open in Google Drive
                  </a>
                  <p className="info-message">
                    Files will appear as they're generated
                  </p>
                </div>
              )}

              {ticket && (
                <div className="status-info">
                  <p><strong>Ticket:</strong> #{ticket}</p>
                  {queuePosition && <p><strong>Queue Position:</strong> {queuePosition}</p>}
                  {estimatedTime && <p><strong>Estimated Time:</strong> {estimatedTime}</p>}
                  <p><strong>Status:</strong> {status || 'processing'}</p>
                </div>
              )}

              <p className="info-message">
                This page will automatically update when documentation is complete.
              </p>
            </div>
          </div>
        )}

        {step === 3 && (
          <div className="step-container">
            <h2>All Done!</h2>
            <div className="success-box">
              <svg className="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
                <circle className="checkmark-circle" cx="26" cy="26" r="25" fill="none"/>
                <path className="checkmark-check" fill="none" d="M14.1 27.2l7.1 7.2 16.7-16.8"/>
              </svg>
              <p>Documentation has been generated and shared to your Google Drive!</p>
              <p className="email-info">Shared with: <strong>{email}</strong></p>

              {driveLink && (
                <div className="drive-link-box">
                  <p><strong>Access your documentation folder:</strong></p>
                  <a
                    href={driveLink}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="drive-link"
                  >
                    Open in Google Drive
                  </a>
                  <p className="link-text">{driveLink}</p>
                </div>
              )}

              {masterDocLink && (
                <div className="drive-link-box">
                  <p><strong>Master Documentation Index:</strong></p>
                  <a
                    href={masterDocLink}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="drive-link"
                  >
                    Open Master Doc
                  </a>
                </div>
              )}

              <div className="completion-info">
                <p><strong>Repository:</strong> {githubUrl}</p>
                <p><strong>Folder Name:</strong> {folderName}</p>
                {ticket && <p><strong>Ticket:</strong> #{ticket}</p>}
              </div>
            </div>
            <button
              onClick={handleReset}
              className="btn btn-secondary"
            >
              Generate Another Documentation
            </button>
          </div>
        )}

        {message && <p className="message success">{message}</p>}
        {error && <p className="message error">{error}</p>}

        <div className="api-docs-section">
          <button
            className="api-docs-link"
            onClick={() => setShowApiDocs(true)}
          >
            API Docs
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import confetti from 'canvas-confetti';
import './App.css';

function App() {
  const [step, setStep] = useState(1);
  const [githubUrl, setGithubUrl] = useState('');
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [driveLink, setDriveLink] = useState('');
  const [timeRemaining, setTimeRemaining] = useState(30);

  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  // Timer effect for 30-second countdown
  useEffect(() => {
    if (step === 2 && timeRemaining > 0) {
      const timer = setTimeout(() => {
        setTimeRemaining(timeRemaining - 1);
      }, 1000);
      return () => clearTimeout(timer);
    } else if (step === 2 && timeRemaining === 0) {
      // Automatically show email form after timer expires
      setMessage('Documentation generation in progress! Enter your email to get access.');

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
    }
  }, [step, timeRemaining]);

  const handleGenerateDocs = async (e) => {
    e.preventDefault();
    setGenerating(true);
    setError('');
    setMessage('');

    try {
      const response = await axios.post(`${API_BASE_URL}/api/generate-docs`, {
        githubUrl
      });

      if (response.data.success) {
        setDriveLink(response.data.driveLink);
        setMessage('Folder created! Documentation is being generated...');
        setTimeRemaining(30); // Reset timer
        setStep(2); // Move to loading/timer step
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create folder');
    } finally {
      setGenerating(false);
    }
  };

  const handleSubmitEmail = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setMessage('');

    try {
      const response = await axios.post(`${API_BASE_URL}/api/share-docs`, {
        githubUrl,
        email
      });

      if (response.data.success) {
        setMessage('Documentation folder shared to your Google Drive!');
        setStep(3); // Move to success page immediately
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to share documentation');
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
    setTimeRemaining(30);
  };

  return (
    <div className="App">
      <div className="container">
        <h1>NYC Code</h1>
        <p className="subtitle">Generate Documentation for GitHub Repositories</p>

        {step === 1 && (
          <div className="step-container">
            <h2>Step 1: Enter GitHub Repository URL</h2>
            <form onSubmit={handleGenerateDocs}>
              <input
                type="url"
                className="input-field"
                placeholder="https://github.com/openai/openai-python"
                value={githubUrl}
                onChange={(e) => setGithubUrl(e.target.value)}
                required
              />
              <button
                type="submit"
                className="btn btn-primary"
                disabled={generating}
              >
                {generating ? 'Generating...' : 'Generate Documentation'}
              </button>
            </form>
          </div>
        )}

        {step === 2 && (
          <div className="step-container">
            <h2>Generating Your Documentation...</h2>
            <div className="timer-container">
              <div className="spinner"></div>
              <p className="timer-text">
                Your documentation folder has been created and is being populated with content.
              </p>
              <div className="countdown">
                <span className="time-number">{timeRemaining}</span>
                <span className="time-label">seconds remaining</span>
              </div>
              <p className="info-message">
                The documentation is processing...
              </p>
            </div>
            {timeRemaining === 0 && (
              <div className="email-section">
                <h3>Almost Done!</h3>
                <p className="success-message">
                  Enter your email to get instant access to your documentation folder
                </p>
                <form onSubmit={handleSubmitEmail}>
                  <input
                    type="email"
                    className="input-field"
                    placeholder="your.email@example.com"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                  <button
                    type="submit"
                    className="btn btn-primary"
                    disabled={loading}
                  >
                    {loading ? 'Sharing...' : 'Share to My Google Drive (Free)'}
                  </button>
                </form>
              </div>
            )}
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
              <p>Documentation has been shared to your Google Drive!</p>
              <p className="email-info">Check your email: <strong>{email}</strong></p>

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

        <div className="repo-info">
          {githubUrl && <p><strong>Repository:</strong> {githubUrl}</p>}
        </div>
      </div>
    </div>
  );
}

export default App;

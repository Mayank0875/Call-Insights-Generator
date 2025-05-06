import React, { useState } from 'react';
import './App.css';
import ReactMarkdown from 'react-markdown';

function Home() {
  const [audioFile, setAudioFile] = useState(null);
  const [audioUrl, setAudioUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [uploadMethod, setUploadMethod] = useState('file');

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('audio/')) {
      setAudioFile(file);
      setError('');
    } else if (file) {
      setError('Please select a valid audio file.');
      setAudioFile(null);
    }
  };

  const handleUrlChange = (e) => {
    setAudioUrl(e.target.value);
  };

  const handleUploadMethodChange = (method) => {
    setUploadMethod(method);
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    setLoading(true);

    try {
      let response;

      if (uploadMethod === 'file') {
        if (!audioFile) {
          setError('Please select an audio file to upload');
          setLoading(false);
          return;
        }

        const formData = new FormData();
        formData.append('file', audioFile);

        response = await fetch('http://localhost:8000/process-audio/', {
          method: 'POST',
          body: formData,
        });
      } else {
        if (!audioUrl) {
          setError('Please enter an audio URL');
          setLoading(false);
          return;
        }

        response = await fetch('http://localhost:8000/process-audio-url/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ url: audioUrl }),
        });
      }

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to process audio');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'An error occurred while processing the audio');
    } finally {
      setLoading(false);
    }
  };


  const renderFormattedConversation = (text) => {
    if (!text) return null;
    
    const lines = text.split('\n');
    
    return (
      <div className="conversation-container">
        {lines.map((line, index) => {
          const isCustomer = line.startsWith('Customer:');
          const isAgent = line.startsWith('Agent:');
          
          if (isCustomer || isAgent) {
            const [speaker, ...contentParts] = line.split(':');
            const content = contentParts.join(':').trim();
            
            return (
              <div 
                key={index} 
                className={`conversation-line ${isCustomer ? 'customer-line' : 'agent-line'}`}
              >
                <span className={`speaker-label ${isCustomer ? 'customer-speaker' : 'agent-speaker'}`}>
                  {speaker}:
                </span>
                <span className="conversation-content">{content}</span>
              </div>
            );
          } else {
            return <div key={index} className="conversation-line">{line}</div>;
          }
        })}
      </div>
    );
  };


  const renderFormattedText = (text) => {
    return <ReactMarkdown>{text}</ReactMarkdown>;
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Call Insights Generator</h1>
      </header>
      <main>
        <div className="upload-container">
          <div className="upload-methods">
            <button 
              className={uploadMethod === 'file' ? 'active' : ''} 
              onClick={() => handleUploadMethodChange('file')}
            >
              Upload Audio File
            </button>
            <button 
              className={uploadMethod === 'url' ? 'active' : ''}
              onClick={() => handleUploadMethodChange('url')}
            >
              Provide Audio URL
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            {uploadMethod === 'file' ? (
              <div className="form-group">
                <label htmlFor="audio-file">Select Audio File:</label>
                <input
                  type="file"
                  id="audio-file"
                  accept="audio/*"
                  onChange={handleFileChange}
                />
                {audioFile && (
                  <div className="file-info">
                    <p>Selected file: {audioFile.name}</p>
                  </div>
                )}
              </div>
            ) : (
              <div className="form-group">
                <label htmlFor="audio-url">Audio URL:</label>
                <input
                  type="text"
                  id="audio-url"
                  value={audioUrl}
                  onChange={handleUrlChange}
                  placeholder="https://example.com/audio.mp3"
                />
              </div>
            )}

            <button type="submit" disabled={loading}>
              {loading ? 'Processing...' : 'Analyze Audio'}
            </button>
          </form>

          {error && <div className="error-message">{error}</div>}
        </div>

        {result && (
          <div className="results-container">
            <h2>Analysis Results</h2>
            
            <div className="result-section">
              <h3>Conversation Transcript</h3>
              <div className="result-content conversation-content">
                {renderFormattedConversation(result.separate_format)}
              </div>
            </div>
            
            <div className="result-section">
              <h3>Conversation Summary</h3>
              <div className="result-content">
                {renderFormattedText(result.summary)}
              </div>
            </div>
            
            <div className="result-section">
              <h3>Agent Performance and Improvement Area's</h3>
              <div className="result-content">
                {renderFormattedText(result.performance)}
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default Home;
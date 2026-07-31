import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router-dom';
import { UploadCloud, CheckCircle, FileText, MoreVertical, Share, Smartphone, Sparkles } from 'lucide-react';
import { uploadChat, loadDemoChatSession } from '../../utils/api';
import './ChatUpload.css';

export default function ChatUpload() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const navigate = useNavigate();

  const onDrop = useCallback(acceptedFiles => {
    if (acceptedFiles?.length > 0) {
      handleUpload(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/plain': ['.txt']
    },
    maxSize: 50 * 1024 * 1024, // 50MB
    multiple: false
  });

  const handleUpload = async (selectedFile) => {
    setFile(selectedFile);
    setUploading(true);
    
    let currentProgress = 0;
    const interval = setInterval(() => {
      currentProgress += 10;
      setProgress(currentProgress);
      
      if (currentProgress >= 100) {
        clearInterval(interval);
        setTimeout(() => {
          setUploading(false);
          navigate('/dashboard');
        }, 600);
      }
    }, 80);

    try {
      await uploadChat(selectedFile);
    } catch (e) {
      console.warn('Upload error:', e);
    }
  };

  const handleLoadSample = async () => {
    setUploading(true);
    setProgress(50);
    try {
      await loadDemoChatSession();
      setProgress(100);
      setTimeout(() => {
        setUploading(false);
        navigate('/dashboard');
      }, 500);
    } catch (e) {
      console.error(e);
      setUploading(false);
    }
  };

  return (
    <div className="upload-container animate-fade-in" id="upload-page">
      <div className="hero-section">
        <h1 className="hero-title">Upload Your WhatsApp Chat</h1>
        <p className="hero-subtitle">Get AI-powered insights, sentiment analysis, and summaries instantly.</p>
      </div>

      <div className="upload-card card" id="dropzone-card">
        {!file && !uploading ? (
          <div 
            {...getRootProps()} 
            className={`dropzone ${isDragActive ? 'active' : ''}`}
            id="file-dropzone"
          >
            <input {...getInputProps()} />
            <div className="dropzone-content">
              <div className="upload-icon-wrapper">
                <UploadCloud size={48} className="upload-icon" />
              </div>
              <h3>{isDragActive ? "Drop file here..." : "Drag & drop your .txt file here"}</h3>
              <p className="file-info">Supported format: .txt (Max 50MB)</p>
              <div className="divider"><span>OR</span></div>
              <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', flexWrap: 'wrap' }}>
                <button className="btn btn-primary" type="button">
                  Browse Files
                </button>
                <button 
                  className="btn" 
                  type="button"
                  onClick={(e) => { e.stopPropagation(); handleLoadSample(); }}
                  style={{ background: 'var(--bg-main)', border: '1px solid var(--primary)', color: 'var(--primary-darker)', fontWeight: '700', display: 'flex', alignItems: 'center', gap: '6px' }}
                >
                  <Sparkles size={16} />
                  <span>Try Sample Chat Demo</span>
                </button>
              </div>
            </div>
          </div>
        ) : (
          <div className="upload-progress-container animate-slide-up">
            <div className="file-success-icon">
              {progress < 100 ? <FileText size={40} className="pulse" /> : <CheckCircle size={40} className="success" />}
            </div>
            <h3>{progress < 100 ? 'Analyzing Chat...' : 'Upload Complete!'}</h3>
            <p className="filename">{file?.name || 'Sample_Project_Chat_Export.txt'}</p>
            <div className="progress-bar-bg">
              <div 
                className="progress-bar-fill" 
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <p className="progress-text">{progress}%</p>
          </div>
        )}
      </div>

      <div className="guide-section">
        <h2 className="guide-title">How to Export WhatsApp Chat</h2>
        <div className="wizard-steps">
          <div className="wizard-card card animate-slide-up" style={{ animationDelay: '0.1s' }}>
            <div className="step-number">1</div>
            <div className="step-icon"><MoreVertical size={24} /></div>
            <h3>Open Menu</h3>
            <p>Open your WhatsApp chat, tap the three dots (⋮) in the top right corner.</p>
          </div>
          
          <div className="wizard-card card animate-slide-up" style={{ animationDelay: '0.2s' }}>
            <div className="step-number">2</div>
            <div className="step-icon"><Smartphone size={24} /></div>
            <h3>Export Chat</h3>
            <p>Select <strong>More</strong> &gt; <strong>Export chat</strong>. Choose <strong>Without Media</strong>.</p>
          </div>
          
          <div className="wizard-card card animate-slide-up" style={{ animationDelay: '0.3s' }}>
            <div className="step-number">3</div>
            <div className="step-icon"><Share size={24} /></div>
            <h3>Save &amp; Upload</h3>
            <p>Save the generated .txt file to your device and upload it here.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

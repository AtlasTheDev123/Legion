import React, { useState, useRef, useEffect } from 'react';
import './VoiceAssistant.css';

/**
 * Voice-Driven AI Assistant Component
 * 
 * Features:
 * - Visual avatar with reactive animations
 * - Voice input with microphone button
 * - Text input fallback
 * - Real-time state transitions with visual feedback
 * - Keyboard shortcuts (Space to record, Esc to cancel)
 * - Fully responsive design
 */

export const VoiceAssistant = ({ onSendMessage = null, onError = null }) => {
  const [state, setState] = useState('idle'); // idle, listening, processing, responding, error
  const [messages, setMessages] = useState([
    { id: 1, text: '👋 Hello! I\'m your AI assistant. Click the microphone or type to get started.', sender: 'assistant' }
  ]);
  const [textInput, setTextInput] = useState('');
  const [transcript, setTranscript] = useState('Listening ready...');
  const [isRecording, setIsRecording] = useState(false);

  const recognitionRef = useRef(null);
  const chatAreaRef = useRef(null);
  const messageIdRef = useRef(2);

  // Initialize Web Speech API
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = true;
      recognitionRef.current.language = 'en-US';

      recognitionRef.current.onstart = () => {
        setState('listening');
        setIsRecording(true);
        setTranscript('Recording...');
      };

      recognitionRef.current.onresult = (event) => {
        let interimTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            if (transcript.trim()) {
              processUserMessage(transcript.trim());
            }
          } else {
            interimTranscript += transcript;
          }
        }
        setTranscript(interimTranscript || 'Recording...');
      };

      recognitionRef.current.onerror = (event) => {
        setState('error');
        handleError(`Speech recognition error: ${event.error}`);
        setTimeout(() => setState('idle'), 2000);
      };

      recognitionRef.current.onend = () => {
        setIsRecording(false);
        setTranscript('');
      };
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.abort();
      }
    };
  }, []);

  // Auto-scroll chat area
  useEffect(() => {
    if (chatAreaRef.current) {
      chatAreaRef.current.scrollTop = chatAreaRef.current.scrollHeight;
    }
  }, [messages]);

  // Handle keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.code === 'Space' && state === 'idle' && document.activeElement?.tagName !== 'INPUT') {
        e.preventDefault();
        startListening();
      }
      if (e.code === 'Escape' && isRecording) {
        e.preventDefault();
        stopListening();
      }
    };

    const handleKeyUp = (e) => {
      if (e.code === 'Space' && isRecording) {
        e.preventDefault();
        stopListening();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [state, isRecording]);

  const startListening = () => {
    if (recognitionRef.current && state === 'idle') {
      recognitionRef.current.start();
    }
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.abort();
      setIsRecording(false);
      setState('processing');
      setTranscript('');
    }
  };

  const addMessage = (text, sender) => {
    const newMessage = {
      id: messageIdRef.current++,
      text,
      sender,
      timestamp: new Date()
    };
    setMessages(prev => [...prev, newMessage]);
  };

  const handleError = (errorMessage) => {
    console.error('[VoiceAssistant Error]', errorMessage);
    addMessage(`⚠️ ${errorMessage}`, 'assistant');
    if (onError) onError(errorMessage);
  };

  const processUserMessage = async (userText) => {
    setIsRecording(false);
    setState('listening');
    setTranscript('');

    // Add user message
    addMessage(userText, 'user');

    // Transition to processing
    setTimeout(() => {
      setState('processing');
    }, 300);

    // Simulate AI response (replace with actual API call)
    try {
      if (onSendMessage) {
        const response = await onSendMessage(userText);
        
        setState('responding');
        addMessage(response, 'assistant');

        // Simulate speech duration
        setTimeout(() => {
          setState('idle');
        }, Math.min(response.length * 50, 5000));
      } else {
        // Default response for demo
        const responses = [
          'That\'s interesting! Tell me more.',
          'I understand. How can I help?',
          'Got it. What would you like me to do?',
          'Absolutely! Let\'s work on that.'
        ];
        const response = responses[Math.floor(Math.random() * responses.length)];

        setState('responding');
        addMessage(response, 'assistant');

        setTimeout(() => {
          setState('idle');
        }, 3000);
      }
    } catch (error) {
      handleError(error.message);
      setState('error');
      setTimeout(() => setState('idle'), 2000);
    }
  };

  const handleMicButtonClick = async () => {
    if (state === 'listening') {
      stopListening();
    } else if (state === 'idle') {
      startListening();
    }
  };

  const handleTextInputChange = (e) => {
    setTextInput(e.target.value);
  };

  const handleTextInputKeyDown = (e) => {
    if (e.key === 'Enter' && textInput.trim() && state === 'idle') {
      const text = textInput.trim();
      setTextInput('');
      setState('processing');
      setTimeout(() => processUserMessage(text), 300);
    }
  };

  const handleAvatarClick = () => {
    if (state === 'idle') {
      startListening();
    }
  };

  const isDisabled = state === 'processing' || state === 'responding';
  const micButtonClass = `mic-button ${isRecording ? 'recording' : ''}`;
  const avatarClass = `avatar ${state}`;
  const statusIndicatorClass = `status-indicator ${state}`;
  const transcriptClass = `transcript ${transcript && transcript !== 'Listening ready...' ? 'active' : ''}`;

  const STATUS_MESSAGES = {
    idle: 'Ready',
    listening: 'Listening...',
    processing: 'Processing...',
    responding: 'Speaking...',
    error: 'Error'
  };

  return (
    <div className="voice-assistant-container">
      <div className="voice-assistant">
        <div className="header">
          <h1>🎤 Voice Assistant</h1>
          <p>Click the microphone to speak</p>
        </div>

        <div className="chat-area" ref={chatAreaRef}>
          {messages.map(msg => (
            <div key={msg.id} className={`chat-message ${msg.sender}`}>
              {msg.text}
            </div>
          ))}
        </div>

        <div className="avatar-section">
          <div className="avatar-container">
            <div 
              className={avatarClass}
              onClick={handleAvatarClick}
              role="button"
              tabIndex={0}
              title="Click to speak"
            >
              🤖
            </div>
          </div>

          <div className={statusIndicatorClass}>
            <div className="status-dot"></div>
            <span className="status-text">{STATUS_MESSAGES[state]}</span>
          </div>
        </div>

        <div className={transcriptClass}>
          {transcript || 'Listening ready...'}
        </div>

        <div className="controls">
          <button
            className={micButtonClass}
            onClick={handleMicButtonClick}
            disabled={isDisabled}
            title="Hold to record or click to toggle"
            aria-label="Microphone button"
          >
            🎤
          </button>
          <input
            type="text"
            className="text-input"
            value={textInput}
            onChange={handleTextInputChange}
            onKeyDown={handleTextInputKeyDown}
            disabled={isDisabled}
            placeholder="Or type your message..."
            aria-label="Message input"
          />
        </div>

        <div className="key-hint">
          Press <kbd>Space</kbd> to record • <kbd>Esc</kbd> to cancel
        </div>
      </div>
    </div>
  );
};

export default VoiceAssistant;

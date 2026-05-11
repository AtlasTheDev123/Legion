/**
 * Voice Control System
 * Handles speech recognition, audio visualization, and voice playback
 */

class VoiceController {
    constructor() {
        this.voiceButton = document.getElementById('voiceButton');
        this.voiceVisualization = document.getElementById('voiceVisualization');
        this.tapHint = document.getElementById('tapHint');
        
        // Configuration
        this.isListening = false;
        this.isProcessing = false;
        this.volume = 70;
        this.speechRate = 1;
        
        // Web Speech API
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        this.recognition.continuous = false;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US';
        
        this.setupRecognition();
        this.setupEventListeners();
        this.setupAudioContext();
    }

    /**
     * Setup speech recognition handlers
     */
    setupRecognition() {
        this.recognition.onstart = () => {
            console.log('Speech recognition started');
            this.isListening = true;
            this.voiceButton.classList.add('listening');
            this.voiceVisualization.classList.add('active');
            this.tapHint.textContent = 'Listening...';
            avatarController.startListening();
        };

        this.recognition.onresult = (event) => {
            let transcript = '';
            let isFinal = false;
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcriptSegment = event.results[i][0].transcript;
                transcript += transcriptSegment;
                
                if (event.results[i].isFinal) {
                    isFinal = true;
                }
            }
            
            if (isFinal) {
                console.log('Final transcript:', transcript);
                this.handleVoiceInput(transcript);
            } else {
                console.log('Interim transcript:', transcript);
                this.updateTranscript(transcript, false);
            }
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.handleError(event.error);
        };

        this.recognition.onend = () => {
            console.log('Speech recognition ended');
            this.isListening = false;
            this.voiceButton.classList.remove('listening');
            this.voiceVisualization.classList.remove('active');
            this.tapHint.textContent = 'Tap to speak';
            avatarController.stopListening();
        };
    }

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        this.voiceButton.addEventListener('mousedown', () => this.startListening());
        this.voiceButton.addEventListener('mouseup', () => this.stopListening());
        this.voiceButton.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.startListening();
        });
        this.voiceButton.addEventListener('touchend', (e) => {
            e.preventDefault();
            this.stopListening();
        });

        // Settings
        document.getElementById('settingsButton').addEventListener('click', () => {
            document.getElementById('settingsModal').classList.add('active');
        });

        document.getElementById('closeSettings').addEventListener('click', () => {
            document.getElementById('settingsModal').classList.remove('active');
        });

        document.getElementById('volumeControl').addEventListener('change', (e) => {
            this.volume = e.target.value;
            this.showToast(`Volume: ${e.target.value}%`, 'info');
        });

        document.getElementById('speechRate').addEventListener('change', (e) => {
            this.speechRate = e.target.value;
            this.showToast(`Speech rate: ${e.target.value}x`, 'info');
        });

        // Close modal on outside click
        document.getElementById('settingsModal').addEventListener('click', (e) => {
            if (e.target.id === 'settingsModal') {
                document.getElementById('settingsModal').classList.remove('active');
            }
        });
    }

    /**
     * Setup Web Audio API for visualization
     */
    setupAudioContext() {
        this.audioContext = null;
        this.analyser = null;
        this.dataArray = null;
        this.animationId = null;
    }

    /**
     * Start listening
     */
    startListening() {
        if (this.isProcessing) return;
        
        try {
            this.recognition.start();
            this.visualizeAudio();
        } catch (error) {
            console.error('Error starting recognition:', error);
        }
    }

    /**
     * Stop listening
     */
    stopListening() {
        try {
            this.recognition.stop();
            if (this.animationId) {
                cancelAnimationFrame(this.animationId);
            }
        } catch (error) {
            console.error('Error stopping recognition:', error);
        }
    }

    /**
     * Handle voice input
     */
    handleVoiceInput(transcript) {
        if (!transcript.trim()) {
            this.showToast('No speech detected', 'info');
            return;
        }

        // Add user message to conversation
        this.addMessage('user', transcript);
        
        // Trigger processing
        this.processVoiceInput(transcript);
    }

    /**
     * Process voice input (simulate AI processing)
     */
    async processVoiceInput(input) {
        this.isProcessing = true;
        this.voiceButton.classList.add('processing');
        this.voiceButton.disabled = true;
        avatarController.startProcessing();

        try {
            // Simulate API call to backend
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            // Simulate AI response
            const response = this.generateResponse(input);
            
            // Add assistant message
            this.addMessage('assistant', response);
            
            // Trigger avatar reaction
            await avatarController.playReaction('acknowledgment');
            
            // Speak response if enabled
            if (document.getElementById('autoPlay').checked) {
                this.speakResponse(response);
            }
            
            avatarController.startResponding();
            await new Promise(resolve => setTimeout(resolve, 2000));
            
        } catch (error) {
            console.error('Error processing input:', error);
            this.showToast('Error processing request', 'error');
        } finally {
            this.isProcessing = false;
            this.voiceButton.classList.remove('processing');
            this.voiceButton.disabled = false;
            avatarController.reset();
        }
    }

    /**
     * Generate AI response (simulate)
     */
    generateResponse(input) {
        const responses = [
            `I understood you said: "${input}". That's interesting!`,
            `Got it: "${input}". Let me process that for you.`,
            `You mentioned: "${input}". I'm analyzing this.`,
            `I hear you: "${input}". How can I help with that?`,
            `Understood: "${input}". That's a great question!`
        ];
        
        return responses[Math.floor(Math.random() * responses.length)];
    }

    /**
     * Speak response using Text-to-Speech
     */
    speakResponse(text) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = parseFloat(this.speechRate);
        utterance.volume = this.volume / 100;
        utterance.lang = 'en-US';
        
        utterance.onstart = () => {
            console.log('Speaking...');
            avatarController.talk(utterance.duration || 3000);
        };
        
        utterance.onend = () => {
            console.log('Finished speaking');
        };
        
        window.speechSynthesis.speak(utterance);
    }

    /**
     * Visualize audio
     */
    visualizeAudio() {
        const bars = document.querySelectorAll('.bar');
        let index = 0;
        
        const animateBar = () => {
            const bar = bars[index % bars.length];
            const height = Math.random() * 12 + 8;
            
            bar.style.height = `${height}px`;
            
            index++;
            if (this.isListening) {
                this.animationId = setTimeout(animateBar, 100);
            }
        };
        
        animateBar();
    }

    /**
     * Update transcript display
     */
    updateTranscript(text, isFinal = false) {
        const container = document.getElementById('messagesContainer');
        let transitoryMessage = container.querySelector('.transitory-message');
        
        if (!transitoryMessage) {
            transitoryMessage = document.createElement('div');
            transitoryMessage.className = 'transitory-message user-message';
            transitoryMessage.innerHTML = `<span class="message-text"></span>`;
            container.appendChild(transitoryMessage);
        }
        
        transitoryMessage.querySelector('.message-text').textContent = text;
        
        if (isFinal) {
            transitoryMessage.remove();
        }
    }

    /**
     * Add message to conversation
     */
    addMessage(sender, text) {
        const container = document.getElementById('messagesContainer');
        
        // Remove any transitoryMessage
        const transitory = container.querySelector('.transitory-message');
        if (transitory) transitory.remove();
        
        const messageDiv = document.createElement('div');
        const now = new Date();
        const time = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.className = `${sender}-message`;
        messageDiv.innerHTML = `
            <span class="timestamp">${time}</span>
            <div class="message-text">${this.sanitizeText(text)}</div>
        `;
        
        container.appendChild(messageDiv);
        container.scrollTop = container.scrollHeight;
    }

    /**
     * Sanitize text
     */
    sanitizeText(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Handle error
     */
    handleError(error) {
        const errorMessages = {
            'no-speech': 'No speech detected. Please try again.',
            'network': 'Network error. Please check your connection.',
            'not-allowed': 'Microphone access not allowed.',
            'audio-capture': 'Microphone not available.'
        };
        
        const message = errorMessages[error] || `Error: ${error}`;
        this.showToast(message, 'error');
    }

    /**
     * Show toast notification
     */
    showToast(message, type = 'info') {
        const toast = document.getElementById('toast');
        toast.textContent = message;
        toast.className = `toast show ${type}`;
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 3000);
    }

    /**
     * Reset state
     */
    reset() {
        this.stopListening();
        this.isProcessing = false;
        avatarController.reset();
    }
}

// Initialize voice controller
const voiceController = new VoiceController();

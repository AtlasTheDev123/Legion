/**
 * Avatar Control System
 * Manages facial expressions, eye movements, and emotional states
 */

class AvatarController {
    constructor() {
        this.avatarContainer = document.getElementById('avatarContainer');
        this.leftIris = document.getElementById('leftIris');
        this.rightIris = document.getElementById('rightIris');
        this.leftEyebrow = document.getElementById('leftEyebrow');
        this.rightEyebrow = document.getElementById('rightEyebrow');
        this.mouthLine = document.querySelector('.mouth-line');
        this.statusDot = document.getElementById('statusDot');
        this.statusText = document.getElementById('statusText');
        
        this.currentExpression = 'neutral';
        this.isLooking = false;
        
        // Initialize
        this.setExpression('neutral');
    }

    /**
     * Set emotion expression
     */
    setExpression(expression) {
        // Remove previous state classes
        this.avatarContainer.classList.remove('happy', 'thinking', 'confused', 'surprised');
        
        switch(expression) {
            case 'happy':
                this.avatarContainer.classList.add('happy');
                this.mouthLine.setAttribute('d', 'M 80 140 Q 100 155 120 140');
                this.leftEyebrow.setAttribute('d', 'M 65 70 Q 75 63 85 70');
                this.rightEyebrow.setAttribute('d', 'M 115 70 Q 125 63 135 70');
                break;
                
            case 'thinking':
                this.avatarContainer.classList.add('thinking');
                this.mouthLine.setAttribute('d', 'M 85 138 Q 100 128 115 138');
                this.leftEyebrow.setAttribute('d', 'M 65 70 Q 75 64 85 72');
                this.rightEyebrow.setAttribute('d', 'M 115 72 Q 125 64 135 70');
                break;
                
            case 'confused':
                this.avatarContainer.classList.add('confused');
                this.mouthLine.setAttribute('d', 'M 85 140 Q 100 135 115 140');
                this.leftEyebrow.setAttribute('d', 'M 65 72 Q 75 67 85 70');
                this.rightEyebrow.setAttribute('d', 'M 115 70 Q 125 67 135 72');
                break;
                
            case 'surprised':
                this.mouthLine.setAttribute('d', 'M 95 140 Q 100 155 105 140');
                this.leftEyebrow.setAttribute('d', 'M 65 65 Q 75 55 85 65');
                this.rightEyebrow.setAttribute('d', 'M 115 65 Q 125 55 135 65');
                break;
                
            case 'neutral':
            default:
                this.mouthLine.setAttribute('d', 'M 80 140 Q 100 145 120 140');
                this.leftEyebrow.setAttribute('d', 'M 65 70 Q 75 65 85 70');
                this.rightEyebrow.setAttribute('d', 'M 115 70 Q 125 65 135 70');
        }
        
        this.currentExpression = expression;
    }

    /**
     * Look at a position (eye movement)
     */
    lookAt(x, y) {
        if (this.isLooking) return;
        
        // Calculate eye direction
        const container = this.avatarContainer.getBoundingClientRect();
        const centerX = container.left + container.width / 2;
        const centerY = container.top + container.height / 2;
        
        const angle = Math.atan2(y - centerY, x - centerX);
        const distance = 4; // Iris movement range
        
        const irisX = Math.cos(angle) * distance;
        const irisY = Math.sin(angle) * distance;
        
        this.leftIris.setAttribute('cx', 75 + irisX);
        this.leftIris.setAttribute('cy', 85 + irisY);
        this.rightIris.setAttribute('cx', 125 + irisX);
        this.rightIris.setAttribute('cy', 85 + irisY);
    }

    /**
     * Reset eyes to center
     */
    resetEyes() {
        this.leftIris.setAttribute('cx', '75');
        this.leftIris.setAttribute('cy', '85');
        this.rightIris.setAttribute('cx', '125');
        this.rightIris.setAttribute('cy', '85');
    }

    /**
     * Nod animation
     */
    nod(count = 1) {
        return new Promise(resolve => {
            const head = document.querySelector('.head');
            let nodCount = 0;
            
            const nodInterval = setInterval(() => {
                nodCount++;
                const progress = (nodCount % 2) * 0.15;
                head.style.transform = `translateY(${progress}px) rotateX(${progress * 5}deg)`;
                
                if (nodCount >= count * 2) {
                    clearInterval(nodInterval);
                    head.style.transform = 'translateY(0) rotateX(0deg)';
                    resolve();
                }
            }, 200);
        });
    }

    /**
     * Blink animation
     */
    blink(count = 1) {
        return new Promise(resolve => {
            const eyes = document.querySelector('.eyes');
            let blinkCount = 0;
            
            const blink = () => {
                eyes.style.transform = 'scaleY(0.1)';
                setTimeout(() => {
                    eyes.style.transform = 'scaleY(1)';
                    blinkCount++;
                    
                    if (blinkCount < count) {
                        setTimeout(blink, 150);
                    } else {
                        resolve();
                    }
                }, 100);
            };
            
            blink();
        });
    }

    /**
     * Start listening state
     */
    startListening() {
        this.avatarContainer.classList.add('listening');
        this.setExpression('thinking');
        this.updateStatus('listening', 'Listening...');
    }

    /**
     * Stop listening state
     */
    stopListening() {
        this.avatarContainer.classList.remove('listening');
        this.setExpression('neutral');
    }

    /**
     * Start processing state
     */
    startProcessing() {
        this.avatarContainer.classList.add('processing');
        this.setExpression('thinking');
        this.updateStatus('processing', 'Processing...');
    }

    /**
     * Stop processing state
     */
    stopProcessing() {
        this.avatarContainer.classList.remove('processing');
    }

    /**
     * Start responding state
     */
    startResponding() {
        this.avatarContainer.classList.remove('processing', 'listening');
        this.setExpression('happy');
        this.updateStatus('responding', 'Responding...');
    }

    /**
     * Reset to idle state
     */
    reset() {
        this.avatarContainer.classList.remove('listening', 'processing');
        this.setExpression('neutral');
        this.resetEyes();
        this.updateStatus('idle', 'Ready');
    }

    /**
     * Update status indicator
     */
    updateStatus(state, text) {
        this.statusDot.classList.remove('idle', 'listening', 'processing', 'responding');
        this.statusDot.classList.add(state);
        this.statusText.textContent = text;
    }

    /**
     * Play reaction sequence
     */
    async playReaction(reaction = 'acknowledgment') {
        switch(reaction) {
            case 'acknowledgment':
                await this.nod(1);
                break;
            case 'confused':
                this.setExpression('confused');
                await this.blink(2);
                this.setExpression('neutral');
                break;
            case 'excited':
                this.setExpression('happy');
                await this.nod(2);
                await this.blink(1);
                break;
        }
    }

    /**
     * Idle animation loop (subtle)
     */
    playIdleAnimation() {
        const sequence = async () => {
            // Random blink
            if (Math.random() > 0.7) {
                await this.blink(1);
            }
            
            // Subtle look around
            if (Math.random() > 0.8) {
                const randomX = Math.random() * window.innerWidth;
                const randomY = Math.random() * window.innerHeight * 0.5;
                this.lookAt(randomX, randomY);
                
                setTimeout(() => {
                    this.resetEyes();
                }, 2000);
            }
        };
        
        setInterval(sequence, 4000);
    }

    /**
     * Simulate talking animation
     */
    talk(duration = 3000) {
        const mouth = document.querySelector('.mouth');
        const startTime = Date.now();
        
        const animate = () => {
            const elapsed = Date.now() - startTime;
            if (elapsed > duration) {
                mouth.style.filter = 'brightness(1)';
                return;
            }
            
            // Mouth opening/closing effect
            const wave = Math.sin((elapsed / 200) * Math.PI) * 0.5;
            mouth.style.filter = `brightness(${1 + wave * 0.2})`;
            
            requestAnimationFrame(animate);
        };
        
        animate();
    }
}

// Initialize avatar controller
const avatarController = new AvatarController();

// Start idle animations
avatarController.playIdleAnimation();

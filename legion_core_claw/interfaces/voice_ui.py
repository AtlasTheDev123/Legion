"""Voice-driven AI Assistant UI with Visual Avatar."""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QTextEdit, QFrame)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QRect, pyqtSignal
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QFont, QPixmap, QIcon
import speech_recognition as sr
import pyttsx3
import threading
import time


class AvatarWidget(QWidget):
    """Visual avatar that reacts to voice input."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)
        self.state = "idle"  # idle, listening, processing, responding
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_frame = 0
        self.nod_angle = 0
        self.eye_open = True
        self.mouth_smile = 0.0

    def set_state(self, state):
        """Set avatar state and start appropriate animation."""
        self.state = state
        if state == "listening":
            self.animation_timer.start(100)  # Faster animation
        elif state == "processing":
            self.animation_timer.start(200)  # Nodding
        elif state == "responding":
            self.animation_timer.start(150)  # Smiling
        else:  # idle
            self.animation_timer.start(500)  # Breathing

    def update_animation(self):
        """Update animation based on current state."""
        self.animation_frame += 1

        if self.state == "listening":
            # Ripple effect and wide eyes
            self.eye_open = True
            self.mouth_smile = 0.0
            self.nod_angle = 0
        elif self.state == "processing":
            # Nodding motion
            self.nod_angle = 10 * (self.animation_frame % 2 - 0.5) * 2
            self.eye_open = True
            self.mouth_smile = 0.0
        elif self.state == "responding":
            # Smiling and blinking
            self.nod_angle = 0
            self.mouth_smile = min(1.0, self.mouth_smile + 0.1)
            if self.animation_frame % 20 == 0:
                self.eye_open = not self.eye_open
        else:  # idle
            # Gentle breathing
            self.nod_angle = 0
            self.eye_open = True
            self.mouth_smile = 0.0

        self.update()

    def paintEvent(self, event):
        """Draw the avatar."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Background circle
        painter.setBrush(QBrush(QColor(215, 204, 200)))  # Warm beige
        painter.setPen(QPen(Qt.NoPen))
        painter.drawEllipse(10, 10, 180, 180)

        # Face outline
        painter.setBrush(QBrush(QColor(241, 215, 196)))  # Lighter skin
        painter.drawEllipse(20, 20, 160, 160)

        # Eyes
        eye_y = 70
        if self.eye_open:
            # Open eyes
            painter.setBrush(QBrush(QColor(139, 69, 19)))  # Brown
            painter.drawEllipse(60, eye_y, 20, 20)
            painter.drawEllipse(120, eye_y, 20, 20)
            # Pupils
            painter.setBrush(QBrush(Qt.black))
            painter.drawEllipse(65, eye_y + 5, 10, 10)
            painter.drawEllipse(125, eye_y + 5, 10, 10)
        else:
            # Blinking
            painter.setPen(QPen(QColor(139, 69, 19), 3))
            painter.drawLine(60, eye_y + 10, 80, eye_y + 10)
            painter.drawLine(120, eye_y + 10, 140, eye_y + 10)

        # Nose
        painter.setPen(QPen(QColor(189, 152, 123), 2))
        painter.drawLine(100, 90, 95, 110)
        painter.drawLine(100, 90, 105, 110)

        # Mouth
        mouth_y = 130
        if self.mouth_smile > 0:
            # Smiling mouth
            painter.setPen(QPen(QColor(165, 42, 42), 3))
            painter.drawArc(75, mouth_y - 10, 50, 20, 0, 180 * 16 * self.mouth_smile)
        else:
            # Neutral mouth
            painter.drawLine(85, mouth_y, 115, mouth_y)

        # Hair
        painter.setBrush(QBrush(QColor(101, 67, 33)))  # Brown hair
        painter.drawEllipse(30, 15, 140, 60)

        # State indicator
        if self.state == "listening":
            # Ripple effect
            alpha = 100 - (self.animation_frame % 10) * 10
            painter.setBrush(QBrush(QColor(66, 165, 245, alpha)))
            painter.setPen(QPen(Qt.NoPen))
            radius = 190 + (self.animation_frame % 5) * 10
            painter.drawEllipse(100 - radius//2, 100 - radius//2, radius, radius)


class VoiceAssistantUI(QWidget):
    """Main voice assistant interface."""

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_voice()
        self.is_listening = False
        self.is_processing = False

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Legion Voice Assistant")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #E3F2FD, stop:1 #F3E5F5);
                color: #424242;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border: none;
                border-radius: 40px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
            QTextEdit {
                background-color: rgba(255, 255, 255, 0.9);
                border: 1px solid #BDBDBD;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QLabel {
                color: #616161;
                font-size: 14px;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout()

        # Status bar at top
        self.status_bar = QFrame()
        self.status_bar.setFixedHeight(5)
        self.status_bar.setStyleSheet("background-color: #81C784; border-radius: 2px;")
        main_layout.addWidget(self.status_bar)

        # Content area
        content_layout = QHBoxLayout()

        # Left side - conversation history
        self.conversation_text = QTextEdit()
        self.conversation_text.setReadOnly(True)
        self.conversation_text.setPlainText("Welcome to Legion Voice Assistant!\n\n")
        content_layout.addWidget(self.conversation_text, 2)

        # Right side - avatar and controls
        right_panel = QVBoxLayout()

        # Avatar
        self.avatar = AvatarWidget()
        right_panel.addWidget(self.avatar, alignment=Qt.AlignCenter)

        # Status label
        self.status_label = QLabel("Ready to listen")
        self.status_label.setAlignment(Qt.AlignCenter)
        right_panel.addWidget(self.status_label)

        # Voice button
        self.voice_button = QPushButton("Tap to Speak")
        self.voice_button.setFixedSize(120, 120)
        self.voice_button.setIcon(QIcon())  # Add microphone icon if available
        self.voice_button.clicked.connect(self.toggle_listening)
        right_panel.addWidget(self.voice_button, alignment=Qt.AlignCenter)

        # Text input (alternative)
        self.text_input = QTextEdit()
        self.text_input.setFixedHeight(60)
        self.text_input.setPlaceholderText("Or type your message here...")
        self.text_input.setVisible(False)
        right_panel.addWidget(self.text_input)

        # Send button
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_text_message)
        self.send_button.setVisible(False)
        right_panel.addWidget(self.send_button)

        content_layout.addLayout(right_panel, 1)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

    def init_voice(self):
        """Initialize voice recognition and synthesis."""
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 180)
        self.engine.setProperty('volume', 0.8)

    def toggle_listening(self):
        """Toggle voice listening."""
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()

    def start_listening(self):
        """Start voice recognition."""
        self.is_listening = True
        self.avatar.set_state("listening")
        self.status_label.setText("Listening...")
        self.voice_button.setText("Listening...")
        self.voice_button.setStyleSheet("""
            QPushButton {
                background-color: #EF5350;
                color: white;
                border: none;
                border-radius: 40px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
            }
        """)

        # Start listening in a separate thread
        threading.Thread(target=self.listen_for_speech, daemon=True).start()

    def stop_listening(self):
        """Stop voice recognition."""
        self.is_listening = False
        self.avatar.set_state("idle")
        self.status_label.setText("Ready to listen")
        self.voice_button.setText("Tap to Speak")
        self.voice_button.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border: none;
                border-radius: 40px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
            }
        """)

    def listen_for_speech(self):
        """Listen for speech input."""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)

            # Process speech
            text = self.recognizer.recognize_google(audio)
            self.process_input(text)

        except sr.WaitTimeoutError:
            self.add_to_conversation("Speech recognition timed out.")
        except sr.UnknownValueError:
            self.add_to_conversation("Could not understand audio.")
        except sr.RequestError as e:
            self.add_to_conversation(f"Speech recognition error: {e}")
        finally:
            self.stop_listening()

    def process_input(self, text):
        """Process user input."""
        self.add_to_conversation(f"You: {text}")
        self.avatar.set_state("processing")
        self.status_label.setText("Processing...")

        # Simulate AI processing (replace with actual Legion integration)
        QTimer.singleShot(2000, lambda: self.respond_to_input(text))

    def respond_to_input(self, user_input):
        """Generate and speak response."""
        # Simple response logic (integrate with Legion AI)
        response = f"I heard: '{user_input}'. How can I help you today?"

        self.add_to_conversation(f"Assistant: {response}")
        self.avatar.set_state("responding")
        self.status_label.setText("Responding...")

        # Speak response
        threading.Thread(target=self.speak_response, args=(response,), daemon=True).start()

        # Reset to idle after speaking
        QTimer.singleShot(3000, lambda: self.avatar.set_state("idle"))
        QTimer.singleShot(3000, lambda: self.status_label.setText("Ready to listen"))

    def speak_response(self, text):
        """Speak the response."""
        self.engine.say(text)
        self.engine.runAndWait()

    def send_text_message(self):
        """Send text message."""
        text = self.text_input.toPlainText().strip()
        if text:
            self.process_input(text)
            self.text_input.clear()

    def add_to_conversation(self, text):
        """Add text to conversation history."""
        current_text = self.conversation_text.toPlainText()
        self.conversation_text.setPlainText(current_text + text + "\n\n")
        # Scroll to bottom
        scrollbar = self.conversation_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def keyPressEvent(self, event):
        """Handle key press events."""
        if event.key() == Qt.Key_Return and event.modifiers() == Qt.ControlModifier:
            # Ctrl+Enter to send text
            self.send_text_message()
        elif event.key() == Qt.Key_F1:
            # F1 to toggle text input
            visible = not self.text_input.isVisible()
            self.text_input.setVisible(visible)
            self.send_button.setVisible(visible)


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("Legion Voice Assistant")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("AtlasTheDev123")

    # Create and show the main window
    window = VoiceAssistantUI()
    window.show()

    # Start the event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
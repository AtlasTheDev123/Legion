# Voice-Driven AI Assistant UI Design Specification

## Overview
A calm, engaging conversational interface featuring a visual avatar that reacts to user voice input with subtle animations and expressions.

---

## Design Principles

1. **Minimalism**: Clean layout with focus on avatar and voice interaction
2. **Calm Aesthetics**: Soft colors, smooth animations, gentle transitions
3. **Visual Feedback**: Clear state indication (listening, processing, responding)
4. **Accessibility**: Large touch targets, clear audio/visual cues
5. **Responsive**: Works on mobile, tablet, and desktop

---

## Color Palette

### Primary Colors
- **Background**: `#F5F7FA` (soft white-blue)
- **Avatar Background**: `#FFFFFF` (pure white)
- **Accent**: `#6C7DFF` (soft purple-blue)
- **Success**: `#4CAF7E` (soft green)
- **Processing**: `#FFB84D` (soft amber)
- **Border**: `#E0E6F2` (light gray-blue)

### Text Colors
- **Primary**: `#2C3E50` (dark blue-gray)
- **Secondary**: `#7F8FA3` (medium gray-blue)
- **Muted**: `#ADB5C7` (light gray-blue)

---

## Layout Structure

```
┌─────────────────────────────────────┐
│     Voice Assistant Interface       │
│                                     │
│  ┌──────────────────────────────┐  │
│  │                              │  │
│  │         [Chat Display]       │  │
│  │    (Conversation History)    │  │
│  │                              │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │    ┌──────────────────────┐  │  │
│  │    │    Visual Avatar    │  │  │
│  │    │  (128x128-256x256)  │  │  │
│  │    │                     │  │  │
│  │    └──────────────────────┘  │  │
│  │                              │  │
│  │  Status: [IDLE/LISTENING/    │  │
│  │           PROCESSING/RES]    │  │
│  │                              │  │
│  │  ┌─────────────┐   ┌──────┐ │  │
│  │  │  Mic Button │   │ Text │ │  │
│  │  │   (Record)  │   │ Input│ │  │
│  │  └─────────────┘   └──────┘ │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

---

## Component Specifications

### 1. **Visual Avatar**
- **Size**: 180x180px (desktop), 140x140px (mobile)
- **Shape**: Circular with soft shadow
- **Background**: Gradient or solid color
- **Animation**: Smooth CSS transitions (0.3s ease)

#### Avatar States:
- **Idle**: Neutral expression, subtle breathing animation
- **Listening**: Eyes tracking, subtle nod animation, glow effect
- **Processing**: Thinking expression, pulsing effect
- **Responding**: Mouth animation, eye contact shifts

### 2. **Status Indicator**
- **Position**: Below avatar
- **Elements**: Status text + visual indicator ring
- **States**:
  - `IDLE`: Gray, no animation
  - `LISTENING`: Blue, pulsing glow
  - `PROCESSING`: Amber, rotating spinner
  - `RESPONDING`: Green, smooth wave animation

### 3. **Voice Input Button**
- **Size**: 64x64px (desktop), 56x56px (mobile)
- **Shape**: Circular
- **Color**: Accent color (soft purple-blue)
- **States**:
  - **Idle**: Static with microphone icon
  - **Recording**: Pulsing animation, red highlight
  - **Hover**: Slight scale up (1.05x), shadow increase

### 4. **Text Input Field**
- **Width**: 100% of container (max 300px)
- **Height**: 44px
- **Border**: Soft, rounded (8px radius)
- **States**:
  - **Idle**: Light border, placeholder text
  - **Focus**: Accent color border, shadow
  - **Disabled**: Grayed out during voice processing

---

## Animation Specifications

### Avatar Animations

#### Breathing (Idle State)
```css
@keyframes breathe {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.02); }
  Animation duration: 4s
  Iteration: infinite
  Easing: ease-in-out
}
```

#### Listening Glow
```css
@keyframes listenerPulse {
  0% { box-shadow: 0 0 0 0 rgba(108, 125, 255, 0.7); }
  70% { box-shadow: 0 0 0 20px rgba(108, 125, 255, 0); }
  100% { box-shadow: 0 0 0 0 rgba(108, 125, 255, 0); }
  Animation duration: 1.5s
  Iteration: infinite
  Easing: ease-out
}
```

#### Processing Throb
```css
@keyframes processThaw {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
  Animation duration: 1s
  Iteration: infinite
  Easing: ease-in-out
}
```

#### Nod Animation
```css
@keyframes nod {
  0%, 100% { transform: rotateX(0deg); }
  25% { transform: rotateX(-8deg); }
  50% { transform: rotateX(0deg); }
  75% { transform: rotateX(-5deg); }
  Animation duration: 0.8s
  Easing: ease-in-out
}
```

### State Transition Cues

| From State  | To State     | Animation                           |
|-------------|--------------|-------------------------------------|
| Idle        | Listening    | Fade in glow + subtle nod           |
| Listening   | Processing   | Freeze glow + add throb effect      |
| Processing  | Responding   | Opacity transition + eye movements  |
| Responding  | Idle         | Gentle fade out, return to breathe  |

---

## Visual Feedback Timeline

```
USER SPEAKS
    ↓
[0.2s] LISTENING state: Avatar glows, pulsing ring appears
       Visual: Blue glow + pulsing indicator
       Audio: Optional subtle beep
    ↓
[During speech] Avatar nods gently every 2-3 seconds
    ↓
USER STOPS SPEAKING
    ↓
[0.3s] PROCESSING state: Glow becomes pulse, avatar thinking pose
       Visual: Amber spinner, avatar eye movement
       Audio: Optional processing sound
    ↓
AI RESPONDS
    ↓
[0.3s] RESPONDING state: Avatar animates mouth, maintains eye contact
       Visual: Green indicator, smooth animations
       Audio: Agent's voice output
    ↓
RESPONSE COMPLETE
    ↓
[0.5s] Return to IDLE state: Gentle fade to normal breathing
```

---

## Responsive Design

### Desktop (1024px+)
- Avatar: 200x200px
- Button size: 72x72px
- Chat area: Full width minus padding
- Layout: Vertical stack, centered

### Tablet (768px - 1023px)
- Avatar: 160x160px
- Button size: 64x64px
- Chat area: 90% width
- Layout: Vertical stack, centered

### Mobile (< 768px)
- Avatar: 120x120px
- Button size: 56x56px
- Chat area: 100% width with 16px padding
- Layout: Full-screen, optimized touch targets

---

## Accessibility Features

1. **Keyboard Support**:
   - Tab navigation through controls
   - Enter/Space to activate microphone
   - Escape to cancel recording

2. **Screen Reader Support**:
   - ARIA labels on all buttons
   - Live region updates for status changes
   - Semantic HTML structure

3. **Visual Indicators**:
   - High contrast colors (WCAG AA)
   - Status text in addition to visual cues
   - Clear focus states on interactive elements

4. **Audio**:
   - Visual transcription of speech
   - On-screen captions for responses
   - Optional haptic feedback for mobile

---

## State Management

### Application States
```
IDLE
 ├─ User can click mic or type
 └─ Avatar in neutral pose

LISTENING
 ├─ Microphone recording
 ├─ Avatar reacts with glow/nod
 └─ Can cancel with Escape key

PROCESSING
 ├─ Speech being recognized/sent
 ├─ Avatar shows thinking pose
 └─ User input disabled

RESPONDING
 ├─ AI response being spoken
 ├─ Avatar animates naturally
 └─ User can interrupt (optional)

ERROR
 ├─ Display error message
 ├─ Avatar shows confused pose
 └─ Reset to IDLE
```

---

## Interaction Patterns

### Voice Input Flow
1. User presses microphone button
2. System transitions to LISTENING
3. Avatar pulses with glow
4. User speaks
5. Avatar nods occasionally
6. User stops speaking
7. System transitions to PROCESSING
8. AI processes and responds
9. Avatar reacts to response
10. System returns to IDLE

### Touch/Keyboard Input Flow
1. User focuses text input field
2. Field highlights with accent border
3. User types message
4. User presses Enter or Send button
5. System transitions to PROCESSING
6. Same as above from step 7

---

## Performance Considerations

- Animations should use CSS transforms (GPU-accelerated)
- Avatar render optimized with requestAnimationFrame
- Microphone permissions handled gracefully
- Audio processing off-loaded to Web Audio API
- Avatar SVG kept lightweight (~10KB)

---

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile Safari 14+
- Chrome for Android

---

## Future Enhancements

1. **Emotion Recognition**: Avatar reacts to sentiment analysis
2. **Eye Tracking**: Avatar follows cursor movement
3. **Multi-language**: Language-specific avatar variations
4. **Customization**: User-selected avatar styles
5. **Accessibility Modes**: High contrast, dyslexia-friendly fonts
6. **Recording History**: Visual transcript of conversations


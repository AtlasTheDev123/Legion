"""Placeholder for voice integration (TTS/STT). No network calls performed by default."""

def text_to_speech(text: str, voice: str = 'default') -> bytes:
    # return empty bytes to indicate placeholder
    return b''


def speech_to_text(audio_bytes: bytes) -> str:
    return ''

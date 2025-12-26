"""Minimal encryption helpers (optional dependency: cryptography)."""

try:
    from cryptography.fernet import Fernet
except Exception:
    Fernet = None


def generate_key() -> str:
    if Fernet is None:
        raise RuntimeError('cryptography not installed')
    return Fernet.generate_key().decode()


def encrypt(text: str, key: str) -> str:
    if Fernet is None: raise RuntimeError('cryptography not installed')
    f = Fernet(key.encode())
    return f.encrypt(text.encode()).decode()


def decrypt(token: str, key: str) -> str:
    if Fernet is None: raise RuntimeError('cryptography not installed')
    f = Fernet(key.encode())
    return f.decrypt(token.encode()).decode()

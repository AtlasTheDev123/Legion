import os

ALLOWED_USERS = os.environ.get("ALLOWED_USERS", "").split(',') if os.environ.get("ALLOWED_USERS") else []
BOT_TOKEN = os.environ.get("BOT_TOKEN")
DEFAULT_AUTH_TOKEN = os.environ.get("DEFAULT_AUTH_TOKEN", "[REDACTED_LAB_AUTH]")

# Small helper to check auth
def is_authorized(user_id: str, token: str) -> bool:
    if not token:
        return False
    if ALLOWED_USERS and user_id not in ALLOWED_USERS:
        return False
    return token == DEFAULT_AUTH_TOKEN

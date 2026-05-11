from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import json, os, sys
from pydantic import BaseModel
from typing import Optional, Dict, Any

# ensure root project path is available for imports
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# import sandbox simulator for safe demos
from bot.sandbox import simulate_execution

app = FastAPI(title="NEXUS Legion Dashboard (dev)")
SCHEMAS = os.path.join(ROOT_DIR, 'schemas', 'functions.json')


@app.get('/api/functions')
async def list_functions():
    try:
        with open(SCHEMAS, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/api/health')
async def health():
    return {'status': 'ok'}


# Serve a minimal single-page UI from dashboard/backend/static
static_dir = os.path.join(os.path.dirname(__file__), 'static')
if os.path.isdir(static_dir):
    app.mount('/', StaticFiles(directory=static_dir, html=True), name='static')


class ChatRequest(BaseModel):
    message: str
    function: Optional[str] = None
    params: Optional[Dict[str, Any]] = None


@app.post('/api/chat')
async def chat(req: ChatRequest):
    """Safe chat endpoint: if `function` provided, simulate execution via sandbox.
    Otherwise echo back a structured response. This endpoint is read-only/simulated.
    """
    if req.function:
        params = req.params or {}
        # Use the sandbox simulator (non-destructive)
        result = simulate_execution(req.function, params)
        return {'ok': True, 'simulated': True, 'result': result}
    # no function: simple echo
    return {'ok': True, 'simulated': False, 'echo': req.message}


class TelegramRequest(BaseModel):
    chat_id: str
    message: str


@app.post('/api/telegram/send')
async def telegram_send(req: TelegramRequest):
    """Send a Telegram message using the bot token if explicitly enabled.

    Safety rules:
    - TELEGRAM_BOT_TOKEN must be set in the environment.
    - ALLOW_TELEGRAM_ACTIONS must be set to '1' to allow real sends. Otherwise the call runs in simulated/dry-run mode.
    - If TELEGRAM_ADMIN_CHAT_ID is set, the server may use it for admin notifications.
    """
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    allow = os.environ.get('ALLOW_TELEGRAM_ACTIONS', '0') == '1'
    if not token:
        raise HTTPException(status_code=403, detail='TELEGRAM_BOT_TOKEN not set. Set this env var to enable Telegram sends in secure environments.')

    # If not explicitly enabled, return a simulated response to avoid accidental messages.
    if not allow:
        return {'ok': True, 'simulated': True, 'detail': f"Dry-run: would send message to {req.chat_id}. Set ALLOW_TELEGRAM_ACTIONS=1 to enable real sends (use in secure env)."}

    # Perform a real send via Telegram API
    import requests

    try:
        resp = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', json={'chat_id': req.chat_id, 'text': req.message}, timeout=10)
        data = resp.json()
        if not data.get('ok'):
            raise HTTPException(status_code=502, detail=f"Telegram API error: {data}")
        return {'ok': True, 'simulated': False, 'telegram': data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class CallRequest(BaseModel):
    phone: str
    message: str


@app.post('/api/telegram/call')
async def telegram_call(req: CallRequest):
    """Call functionality is sensitive. We do NOT place PSTN calls here.

    Behavior:
    - If TELEGRAM_BOT_TOKEN and ALLOW_TELEGRAM_ACTIONS=1 and TELEGRAM_ADMIN_CHAT_ID are set, we will notify the admin via Telegram that a call should be placed.
    - Otherwise returns a simulated/dry-run response.
    """
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    allow = os.environ.get('ALLOW_TELEGRAM_ACTIONS', '0') == '1'
    admin_chat = os.environ.get('TELEGRAM_ADMIN_CHAT_ID')

    if not token or not allow or not admin_chat:
        # Safe default: simulated only
        return {'ok': True, 'simulated': True, 'detail': f"Dry-run: would request call to {req.phone}. To enable notifications set TELEGRAM_BOT_TOKEN, TELEGRAM_ADMIN_CHAT_ID and ALLOW_TELEGRAM_ACTIONS=1."}

    # Send an admin notification via Telegram so an operator can place the call via approved channels
    import requests

    try:
        text = f"[REQUESTED CALL]\nNumber: {req.phone}\nMessage: {req.message[:400]}"
        resp = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', json={'chat_id': admin_chat, 'text': text}, timeout=10)
        data = resp.json()
        if not data.get('ok'):
            raise HTTPException(status_code=502, detail=f"Telegram API error: {data}")
        return {'ok': True, 'simulated': False, 'telegram': data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

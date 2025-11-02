"""Small helper to configure a Telegram bot profile safely.

This script reads TELEGRAM_BOT_TOKEN and ALLOW_TELEGRAM_ACTIONS from the environment.
It will only call Telegram API methods if ALLOW_TELEGRAM_ACTIONS == '1'.

Usage (local):
  copy `.env.example` to `.env`, set TELEGRAM_BOT_TOKEN, set ALLOW_TELEGRAM_ACTIONS=1 (only in a secure environment), then:
    python scripts/telegram_configure_bot.py --description "VEX_X_BOT | NEXUS-LEGION X OMEGA AI"

Do NOT commit your `.env` file.
"""
import os
import sys
import argparse
import requests

API_BASE = "https://api.telegram.org"


def call_telegram(token: str, method: str, payload: dict):
    url = f"{API_BASE}/bot{token}/{method}"
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"ok": False, "error": str(e)}


def set_description(token: str, description: str):
    return call_telegram(token, "setMyDescription", {"description": description})


def set_short_description(token: str, short_desc: str):
    return call_telegram(token, "setMyShortDescription", {"short_description": short_desc})


def set_commands(token: str, commands: list):
    # commands is list of dicts: [{"command":"start","description":"..."}, ...]
    return call_telegram(token, "setMyCommands", {"commands": commands})


def main():
    parser = argparse.ArgumentParser(description="Configure Telegram bot metadata (safe, gated).")
    parser.add_argument('--description', default='', help='Long description for the bot')
    parser.add_argument('--short', default='', help='Short description')
    parser.add_argument('--set-commands', action='store_true', help='Install a small command set')
    args = parser.parse_args()

    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    allow = os.environ.get('ALLOW_TELEGRAM_ACTIONS', '0') == '1'

    if not token:
        print('TELEGRAM_BOT_TOKEN not set. Exiting. Put your token in .env or the environment.')
        sys.exit(1)

    if not allow:
        print('ALLOW_TELEGRAM_ACTIONS != 1. Running in dry-run/simulated mode. No changes will be applied.')
        print('To enable real API calls, set ALLOW_TELEGRAM_ACTIONS=1 in a secure environment.')

    results = {}
    if args.description:
        print('Setting description (dry-run)' if not allow else 'Setting description...')
        res = set_description(token, args.description) if allow else {"ok": True, "simulated": True}
        results['description'] = res

    if args.short:
        print('Setting short description (dry-run)' if not allow else 'Setting short description...')
        res = set_short_description(token, args.short) if allow else {"ok": True, "simulated": True}
        results['short_description'] = res

    if args.set_commands:
        cmds = [
            {"command": "start", "description": "Start interacting with VEX_X_BOT"},
            {"command": "help", "description": "Show help and usage"},
        ]
        print('Installing commands (dry-run)' if not allow else 'Installing commands...')
        res = set_commands(token, cmds) if allow else {"ok": True, "simulated": True}
        results['commands'] = res

    print('\nResult summary:')
    for k, v in results.items():
        print(f"- {k}: {v}")


if __name__ == '__main__':
    main()

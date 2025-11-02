## Telegram integration (VEX_X_BOT)

This repository ships a small dashboard and safe demo endpoints for Telegram-based bots. For security we do NOT commit bot tokens. Follow these steps to integrate a real Telegram bot safely:

1. Create a local `.env` from the provided example and do NOT commit it:

```text
cp .env.example .env
# edit .env and set TELEGRAM_BOT_TOKEN and optionally TELEGRAM_ADMIN_CHAT_ID
```

2. Populate your token securely (example `.env` fields):

```text
TELEGRAM_BOT_TOKEN=your_real_token_here
ALLOW_TELEGRAM_ACTIONS=0    # keep 0 for dry-run; set to 1 only in secured envs
TELEGRAM_ADMIN_CHAT_ID=     # optional: admin chat id for notifications
```

3. By default the dashboard endpoints run in dry-run/simulated mode. To enable real sends/notifications set `ALLOW_TELEGRAM_ACTIONS=1` and ensure the environment is secure (CI or secrets manager). Never commit `.env` to source control.

4. To programmatically set the bot description and commands, use the helper:

```powershell
# (Windows PowerShell example)
copy .\.env.example .\.env
# edit .env to add TELEGRAM_BOT_TOKEN and set ALLOW_TELEGRAM_ACTIONS=1 (secure environment)
python scripts/telegram_configure_bot.py --description "VEX_X_BOT | NEXUS-LEGION X OMEGA AI" --set-commands
```

Security notes:
- Never paste or store tokens in issue trackers, PRs, or committed files.
- Prefer using platform secret stores (GitHub Actions secrets, Azure KeyVault, or OS-level secret stores) in CI and deployments.
- The server endpoints `/api/telegram/send` and `/api/telegram/call` require `TELEGRAM_BOT_TOKEN` and `ALLOW_TELEGRAM_ACTIONS=1` to perform real actions; otherwise they return simulated responses.

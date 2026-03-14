# 📚 Omani Book Bot

A Telegram bot that searches for books across 4 Omani bookstore websites simultaneously and presents results in a clean, bilingual (Arabic/English) interface.

## Overview

The bot allows users to type a book name. It then scrapes all 4 bookstore websites concurrently and returns results from each site showing:
- 📚 Book title
- 💰 Price (with currency)
- ✅/❌ Availability status
- 🖼️ Cover image
- 🛒 Direct buy link (inline button)

### Supported Bookstores

| Store | Website |
|-------|---------|
| Hiber | https://hiber.om/ |
| Thawaqa | https://thawaqa.com/ |
| Rawazin | https://rawazin.om/ |
| Ain Bookstore | https://ainbookstore.com/ |

## Prerequisites

- Python 3.11+
- Docker & Docker Compose (for containerized deployment)
- A Telegram Bot Token

## Get a Bot Token

1. Open Telegram → search **@BotFather** → send `/newbot`
2. Follow the steps and copy the token
3. Paste it into `.env` as `TELEGRAM_BOT_TOKEN`

## Get Your Telegram User ID

1. Open Telegram → search **@userinfobot** → start it
2. It replies with your numeric user ID
3. Add it to `ALLOWED_USER_IDS` and `ADMIN_USER_IDS` in `.env`

## Setup Without Docker

```bash
git clone <repo>
cd bookbot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your values
python bot.py
```

## Setup With Docker

```bash
cp .env.example .env
# Edit .env with your values
docker-compose up -d --build
docker-compose logs -f
```

## Stopping the Bot

```bash
docker-compose down
```

## Moving to a New VPS

1. Copy the entire `bookbot/` folder including `.env`
2. Install Docker and Docker Compose on the new machine
3. Run: `docker-compose up -d --build`

## Bot Commands

| Command | Description |
|---------|-------------|
| `/start` | Welcome message + language selection |
| `/help` | Usage instructions |
| `/search <book name>` | Search for a book |
| `/language` | Change language (AR/EN) |
| *Any text* | Also triggers a search |

## Admin Commands

| Command | Description |
|---------|-------------|
| `/whitelist` | List all whitelisted user IDs |
| `/adduser <id>` | Add a user at runtime (update `.env` for persistence) |
| `/removeuser <id>` | Remove a user at runtime (update `.env` for persistence) |
| `/status` | Show security mode and user counts |

## Viewing Logs

```bash
# Live general log (Docker):
docker exec omani_bookbot tail -f logs/bot.log

# Live unauthorized access log (Docker):
docker exec omani_bookbot tail -f logs/unauthorized.log

# From host machine (volume mounted):
tail -f ./logs/unauthorized.log
```

## Whitelist Modes

| Mode | Behavior |
|------|----------|
| `ALLOWED_USER_IDS` is empty | 🔓 **Open mode**: anyone can use the bot |
| `ALLOWED_USER_IDS` has IDs | 🔒 **Whitelist mode**: only listed users can access |

Unauthorized users are **silently ignored** with no response.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather | *(required)* |
| `ALLOWED_USER_IDS` | Comma-separated allowed user IDs | *(empty = open mode)* |
| `ADMIN_USER_IDS` | Comma-separated admin user IDs | *(empty)* |
| `LOG_LEVEL` | Logging level | `INFO` |
| `LOG_UNAUTHORIZED` | Log unauthorized attempts | `true` |
| `REQUEST_TIMEOUT` | Scraper request timeout (seconds) | `15` |
| `MAX_RESULTS_PER_SITE` | Max results per bookstore | `3` |

## License

MIT

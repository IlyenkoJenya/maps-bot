# Aquasoft Astana — Review Bot

A Telegram bot for generating 2GIS and Google Maps reviews. Uses real photos from technician visits and job data to create unique, human-like reviews via OpenAI GPT.

## What it does

- A technician sends `/start` and selects a platform (2GIS / Google Maps / text only)
- The bot sends a real job photo + platform review link
- GPT generates 3 review variants: short, medium, long
- Reviews alternate between Russian and Kazakh
- Used photos are removed from the pool (never repeated)

## Stack

- Python 3.11+
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) 22.x
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- Docker

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/aquasoft-maps-bot.git
cd aquasoft-maps-bot
```

### 2. Create `.env`

```bash
cp .env.example .env
```

Fill in `.env`:

```env
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
LINK_2GIS=your_2gis_review_link
LINK_GOOGLE_MAPS=your_google_maps_review_link
```

### 3. Add photos and records

Place the following in the project root:

```
photos/
  Astana/
    astana_photos/      ← job visit photos
    photo_records.json  ← job records data
```

`photo_records.json` format:

```json
{
  "filename.jpg": {
    "work_type": "Maintenance",
    "product_type": "AQUASOFT Classic-6",
    "cartridge_type": "Standard",
    "address": "Dostyk St, 1",
    "maintenance_cost": "15000",
    "product_cost": "",
    "comment": "Replaced 3 cartridges"
  }
}
```

### 4. Run locally

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python bot.py
```

### 5. Run with Docker

```bash
docker build -t aquasoft-bot .

docker run -d \
  --name aquasoft-bot \
  --env-file .env \
  -v /path/to/photos:/app/photos \
  --restart unless-stopped \
  aquasoft-bot
```

## Bot commands

| Command | Description |
|---------|-------------|
| `/start` | Start review generation |
| `/review` | Same as `/start` |
| `/status` | Show remaining photo count |

## Project structure

```
├── bot.py              # Telegram bot — commands and button handlers
├── review_generator.py # Review generation via OpenAI
├── data_manager.py     # Photo pool and job records management
├── config.py           # Configuration loaded from .env
├── parse_records.py    # One-time data parsing utility
├── Dockerfile
├── requirements.txt
├── .env.example
└── photos/             # Not in repo — add manually
```

## License

MIT

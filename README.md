# Quadra Unified Api SDK Examples

## Prerequisites
- Python 3.10 or higher
- pip
- Quadra API Keys
- Quadra API URL
- Quadra API Documentation: https://unified-api.quadra.trade/docs

## Installation
For regular usage:
```bash
pip install python-decouple aiohttp asyncio pandas websockets
```
To use telegram bot:
```bash
pip install python-tg-bot --upgrade
```



## General Usage

### Setup
1. Set the BASE_URL, and your API Keys in your .env file.
### Public Endpoints
1. Get supported venues from `src/examples/public/getVenues.py`.
2. Get supported contracts from `src/examples/public/getContracts.py`.
3. Use `exchange_id` and `market_quadra` fields generally to query the public endpoints.

### Account Endpoints
1. Get your own venues from `src/examples/account/getVenues.py`.
2. Use `company_exchange_id` (and `vault_id`) fields to query the account endpoints.


## Telegram Bot
1. Create a telegram bot using BotFather. Go to `src/telegram/TOKEN.MD` for details.
2. Set the TELEGRAM_BOT_TOKEN in your .env file.
3. Run the telegram bot directly from src/telegram/app.py OR
4. Build a docker image and run the bot in a container using 
```bash
docker-compose up --build -d   
```
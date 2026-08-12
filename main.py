import asyncio
import logging
from aiohttp import web

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN, PORT

# Import database initializer
from services.database import init_db

# Import all handler routers
from handlers import start, admin, media, chat

# Enable Logging
logging.basicConfig(level=logging.INFO)

# Async Web Server for Cloud Health Checks (Render / Railway)
async def handle_health_check(request):
    return web.Response(text="Nova-V2 is live and healthy!", status=200)

async def start_health_check_server():
    app = web.Application()
    app.router.add_get("/", handle_health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    logging.info(f"Health check server running on port {PORT}")

async def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        raise ValueError("BOT_TOKEN is missing! Please set it in config.py or .env file.")

    # 1. Initialize SQLite Database
    init_db()

    # 2. Initialize Bot and Dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # -------------------------------------------------------------
    # ROUTER REGISTRATION ORDER IS CRITICAL:
    # 1. start.router  -> Handles /start, /help, & menu buttons
    # 2. admin.router  -> Handles /stats & media reply /broadcast
    # 3. media.router  -> Handles incoming Photos & Voice Notes
    # 4. chat.router   -> Catch-all for AI conversational text (MUST BE LAST)
    # -------------------------------------------------------------
    dp.include_router(start.router)
    dp.include_router(admin.router)
    dp.include_router(media.router)
    dp.include_router(chat.router)

    # 3. Start Async Health Check Server for Web Hosting
    await start_health_check_server()

    logging.info("Starting Nova-V2 Bot Polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot execution stopped.")

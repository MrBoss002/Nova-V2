import asyncio
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

from aiogram import Bot, Dispatcher
from config import BOT_TOKEN, PORT

# Import all handler routers
from handlers import start, admin, media, chat

# Enable Logging
logging.basicConfig(level=logging.INFO)

# Web Server for Cloud Health Checks (Render / Railway)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Nova-V2 is live and healthy!")

def run_health_check_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, HealthCheckHandler)
    logging.info(f"Health check server running on port {PORT}")
    httpd.serve_forever()

async def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        raise ValueError("BOT_TOKEN is missing! Please set it in config.py or .env file.")

    # Initialize Bot and Dispatcher
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

    # Start Health Check Server in Background Thread for web hosting
    Thread(target=run_health_check_server, daemon=True).start()

    logging.info("Starting Nova-V2 Bot Polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot execution stopped.")

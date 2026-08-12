import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Credentials
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))

# Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")

# Branding & Owner Config
OWNER_HANDLE = "@MrBoss002"
MAIN_CHANNEL = "@MrBossTG"
STORE_CATALOG = "https://sites.google.com/view/zerotwo-onlinestore"

# Server Port
PORT = int(os.getenv("PORT", 10000))

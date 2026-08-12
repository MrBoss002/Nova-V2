# 🚀 Nova-V2 — Intelligent Telegram AI Assistant & Business Hub

[![GitHub Stars](https://img.shields.io/github/stars/MrBoss002/Nova-V2?style=for-the-badge&color=gold)](https://github.com/MrBoss002/Nova-V2/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/MrBoss002/Nova-V2?style=for-the-badge&color=blue)](https://github.com/MrBoss002/Nova-V2/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/MrBoss002/Nova-V2?style=for-the-badge&color=red)](https://github.com/MrBoss002/Nova-V2/issues)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-brightgreen?style=for-the-badge&logo=python)](https://www.python.org/)

Nova-V2 is a feature-rich, asynchronous Telegram bot built with aiogram 3, Google Gemini AI, and SQLite. Engineered for channel managers, content creators, and e-commerce founders, Nova-V2 seamlessly handles multimodal AI chat, native Markdown post formatting, voice note transcriptions, media broadcasting, and database user tracking.

---

## ✨ Key Features

* 🧠 Gemini AI Multimodal Processing: High-speed chat, text generation, document analysis, and photo/OCR understanding powered by Google Gemini.
* 🎙️ Voice Note Processing: Direct audio transcription and automated intelligent responses to voice clips.
* ✍️ Native Telegram Header Formatting: Preserves and formats native #, ##, and ### headers in MarkdownV2 for clean visual headers in Telegram clients.
* 📢 Smart Media Broadcast: Clone and broadcast photos, videos, and formatted posts with interactive captions across all bot users using native copy_message.
* 📊 User Analytics & Database Storage: Persistent tracking of registered users in SQLite with an instant /stats system metric summary.
* 🔔 Private Log Channel Alerts: Real-time channel notifications whenever a new user boots up the bot.
* 🌐 Web Health Check Integration: Built-in aiohttp web server running health checks for 24/7 continuous hosting on Render, Railway, or VPS.

---

## 📁 Repository Structure

Nova-V2/
├── handlers/
│   ├── __init__.py      # Package exports for aiogram handlers
│   ├── start.py         # /start menu, persona selection & log channel routing
│   ├── admin.py         # /stats metrics & media reply /broadcast
│   ├── media.py         # Gemini photo/vision & voice note audio handling
│   ├── chat.py          # Dynamic AI conversational text routing & owner responses
│   └── formatter.py     # Native Telegram MarkdownV2 heading & string escape logic
├── services/
│   ├── __init__.py      # Package exports for internal services
│   ├── database.py     # SQLite persistence script for tracking user records
│   └── gemini.py       # Google Gemini API connector & model prompt engine
├── config.py            # Environment configuration settings & default fallbacks
├── main.py              # Master application runner & aiohttp health check server
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation

---

## ⚙️ Environment Variables

Configure these keys in your local .env file or hosting service dashboard:

| Variable | Description | Required |
| :--- | :--- | :---: |
| BOT_TOKEN | Telegram Bot API token from @BotFather | Yes |
| GEMINI_API_KEY | Google AI Studio API key | Yes |
| ADMIN_ID | Your numeric Telegram user ID for admin commands | Yes |
| LOG_CHANNEL_ID | Numeric ID of your private channel for real-time join alerts | Optional |
| PORT | Port for the aiohttp health server (Default: 10000) | Optional |

---

## 🛠️ Admin Commands

The bot includes built-in controls accessible only to the specified ADMIN_ID:

| Command | Action |
| :--- | :--- |
| /stats | View real-time database metric summaries (total users, system status, active engine). |
| /broadcast | Reply to any message, photo, or post with /broadcast to deliver it across all registered users. |

---

## 💻 Local Setup & Execution

1. Clone the repository:
   git clone https://github.com/MrBoss002/Nova-V2.git
   cd Nova-V2

2. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Set up .env file:
   BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyZ
   GEMINI_API_KEY=AIzaSyYourGeminiApiKeyHere
   ADMIN_ID=123456789
   LOG_CHANNEL_ID=-1001234567890
   PORT=10000

5. Launch the bot:
   python main.py

---

## ☁️ Deploy to Render

Deploy Nova-V2 to Render for 24/7 web hosting:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/MrBoss002/Nova-V2)

### Render Deployment Steps:
1. Click the Deploy to Render button above or connect your MrBoss002/Nova-V2 repository manually.
2. Set Environment to Python 3.
3. Set Build Command: pip install -r requirements.txt
4. Set Start Command: python main.py
5. Add your Environment Variables (BOT_TOKEN, GEMINI_API_KEY, ADMIN_ID, PORT=10000) under the Environment tab.
6. Save and deploy!

---

## 🤝 Community & Support

Need help with setup, technical support, or video tutorials? Connect below:

* 👤 **Developer / Technical Contact:** [https://t.me/MrBoss002](https://t.me/MrBoss002)
* 📢 **Official Telegram Channel:** [https://t.me/ZeroTwo_OnlineStore](https://t.me/ZeroTwo_OnlineStore)
* 🎥 **YouTube Video Tutorials:** [https://youtube.com](https://youtube.com)

---

### 📜 License
Distributed under the MIT License. See LICENSE for details.

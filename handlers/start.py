from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import OWNER_HANDLE, MAIN_CHANNEL, STORE_CATALOG, LOG_CHANNEL_ID
from services.database import add_user
import logging

router = Router()

def get_start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="💼 Business Assistant", callback_data="mode_business")
    builder.button(text="✍️ Post Formatter", callback_data="mode_creator")
    builder.button(text="💬 Casual Chat", callback_data="mode_friend")
    builder.button(text="📢 Main Channel", url=f"https://t.me/{MAIN_CHANNEL.replace('@', '')}")
    builder.button(text="🛍️ Visit Store", url=STORE_CATALOG)
    builder.button(text="👤 Developer / Help", url=f"https://t.me/{OWNER_HANDLE.replace('@', '')}")
    builder.adjust(2, 1, 2, 1)
    return builder.as_markup()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    user = message.from_user
    
    # 1. Save user to SQLite Database
    is_new_user = add_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name
    )

    # 2. Send Log Channel alert if new user joins & LOG_CHANNEL_ID is set
    if is_new_user and LOG_CHANNEL_ID:
        try:
            log_text = (
                "🎉 **New User Started Nova-V2!**\n\n"
                f"• **Name:** {user.first_name}\n"
                f"• **Username:** @{user.username if user.username else 'N/A'}\n"
                f"• **User ID:** `{user.id}`"
            )
            await message.bot.send_message(chat_id=LOG_CHANNEL_ID, text=log_text, parse_mode="Markdown")
        except Exception as e:
            logging.error(f"Failed to send log alert: {e}")

    welcome_text = (
        "✨ *Welcome to Nova — Your All-in-One AI Assistant & Business Hub\\!*\n\n"
        "Hey there\\! 👋 I'm Nova, your personal AI assistant, content strategist, and dynamic companion\\. "
        "Whether you need help growing your business, managing Telegram channels, formatting rich posts, or chatting, I'm here for you\\!\n\n"
        "💡 *What I can do:* \n"
        "• 💼 *Business & E\\-Commerce:* Marketing strategies, copy, and roadmaps\n"
        "• 🎨 *Social Media:* High\\-converting captions with key words\n"
        "• ✍️ *Rich Formatting:* Native headers \\(#, ##, ###\\), spoilers, and blocks\n"
        "• 🖼️ *Multimodal:* Analyze photos, extract OCR text, and transcribe voice notes\n"
        "• 🤝 *Owner Routing:* Pointing you to official updates and direct support\n\n"
        "👇 *Pick a mode below or send a message to start\\!*"
    )
    await message.answer(welcome_text, parse_mode="MarkdownV2", reply_markup=get_start_keyboard())

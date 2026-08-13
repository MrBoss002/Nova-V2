import logging
from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import OWNER_HANDLE, MAIN_CHANNEL, STORE_CATALOG, LOG_CHANNEL_ID
from services.database import add_user

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
    try:
        is_new_user = add_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name
        )
    except Exception as e:
        logging.error(f"Database error in cmd_start: {e}")
        is_new_user = False

    # 2. Send Log Channel alert if new user joins & LOG_CHANNEL_ID is set
    if is_new_user and LOG_CHANNEL_ID:
        try:
            log_text = (
                "🎉 <b>New User Started Nova-V2!</b>\n\n"
                f"• <b>Name:</b> {user.first_name}\n"
                f"• <b>Username:</b> @{user.username if user.username else 'N/A'}\n"
                f"• <b>User ID:</b> <code>{user.id}</code>"
            )
            await message.bot.send_message(chat_id=LOG_CHANNEL_ID, text=log_text, parse_mode="HTML")
        except Exception as e:
            logging.error(f"Failed to send log alert: {e}")

    # 3. Welcome text converted to standard HTML (no unescaped character crashes)
    welcome_text = (
        "✨ <b>Welcome to Nova — Your All-in-One AI Assistant & Business Hub!</b>\n\n"
        "Hey there! 👋 I'm Nova, your personal AI assistant, content strategist, and dynamic companion. "
        "Whether you need help growing your business, managing Telegram channels, formatting rich posts, or chatting, I'm here for you!\n\n"
        "💡 <b>What I can do:</b>\n"
        "• 💼 <b>Business & E-Commerce:</b> Marketing strategies, copy, and roadmaps\n"
        "• 🎨 <b>Social Media:</b> High-converting captions with key words\n"
        "• ✍️ <b>Rich Formatting:</b> Native headers (#, ##, ###), spoilers, and blocks\n"
        "• 🖼️ <b>Multimodal:</b> Analyze photos, extract OCR text, and transcribe voice notes\n"
        "• 🤝 <b>Owner Routing:</b> Pointing you to official updates and direct support\n\n"
        "👇 <b>Pick a mode below or send a message to start!</b>"
    )

    try:
        await message.answer(welcome_text, parse_mode="HTML", reply_markup=get_start_keyboard())
    except Exception as e:
        logging.error(f"Failed to send start message to user: {e}")

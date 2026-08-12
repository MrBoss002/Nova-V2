from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import OWNER_HANDLE, MAIN_CHANNEL, STORE_CATALOG

router = Router()

def get_start_keyboard():
    """Generates interactive menu buttons."""
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

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "❓ *Nova Help & Support Center*\n\n"
        "• */start* — Reset chat and open the main menu\n"
        "• */mode* — Switch personas \\(Business, Friend, Creator\\)\n"
        "• */stats* — Admin system metrics\n"
        "• */broadcast* — Admin global announcements\n\n"
        f"Need custom help or reporting a bug? Contact my creator {OWNER_HANDLE} or join {MAIN_CHANNEL}\\!"
    )
    await message.answer(help_text, parse_mode="MarkdownV2")

@router.callback_query(F.data.startswith("mode_"))
async def handle_mode_callback(callback: types.CallbackQuery):
    mode = callback.data.split("_")[1]
    mode_titles = {
        "business": "💼 Business & E-Commerce Mode",
        "creator": "✍️ Post Formatter & Content Mode",
        "friend": "💬 Casual Friend Mode"
    }
    selected = mode_titles.get(mode, "Default Mode")
    await callback.message.answer(f"✅ Switched to **{selected}**! How can I help you in this mode?", parse_mode="Markdown")
    await callback.answer()
  

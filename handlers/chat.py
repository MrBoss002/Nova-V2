from aiogram import Router, types
from aiogram.enums import ParseMode
from services.gemini import generate_response
from handlers.formatter import format_telegram_md, escape_md_v2
from config import OWNER_HANDLE, MAIN_CHANNEL

router = Router()

@router.message()
async def handle_text_message(message: types.Message):
    # Ignore commandshandled by other routers
    if message.text and message.text.startswith('/'):
        return

    # Show typing indicator while generating AI response
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    user_text = message.text

    # Route owner or channel questions explicitly
    lower_text = user_text.lower()
    if any(q in lower_text for q in ["who created you", "who made you", "who is your owner", "who is your developer"]):
        owner_reply = (
            f"I was created by **Muhammad Risvan C** ({OWNER_HANDLE})\\!\n"
            f"For official announcements, updates, and support, join our channel: {MAIN_CHANNEL}"
        )
        await message.answer(owner_reply, parse_mode=ParseMode.MARKDOWN_V2)
        return

    # Generate response from Gemini API
    ai_response = await generate_response(prompt=user_text)

    # Format output to ensure safe MarkdownV2 rendering for Telegram
    formatted_response = format_telegram_md(ai_response)

    try:
        await message.answer(formatted_response, parse_mode=ParseMode.MARKDOWN_V2)
    except Exception:
        # Fallback to plain text if syntax escaping fails
        await message.answer(ai_response)

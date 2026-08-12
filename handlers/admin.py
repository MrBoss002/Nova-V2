from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from config import ADMIN_ID
from services.database import get_all_users, get_user_count

router = Router()

@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    total_users = get_user_count()
    stats_text = (
        "📊 *Nova\\-V2 System Metrics*\n\n"
        f"• *Total Users Registered:* `{total_users}` Users\n"
        "• *AI Engine:* Google Gemini 1\\.5 Flash\n"
        "• *Status:* 🟢 Operational"
    )
    await message.answer(stats_text, parse_mode="MarkdownV2")

@router.message(Command("broadcast"))
async def cmd_broadcast(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    if not message.reply_to_message:
        await message.answer(
            "⚠️ **How to Broadcast Media:**\n\n"
            "1. Upload your photo/video/text with desired formatting.\n"
            "2. **Reply** to that message with `/broadcast`."
        )
        return

    target_message = message.reply_to_message
    users = get_all_users()
    successful, failed = 0, 0

    await message.answer(f"📢 Starting broadcast to `{len(users)}` users...")

    for user_id in users:
        try:
            await message.bot.copy_message(
                chat_id=user_id,
                from_chat_id=message.chat.id,
                message_id=target_message.message_id
            )
            successful += 1
        except Exception:
            failed += 1

    summary = (
        "✅ *Broadcast Complete*\n\n"
        f"• *Successful:* `{successful}`\n"
        f"• *Failed/Blocked:* `{failed}`"
    )
    await message.answer(summary, parse_mode="MarkdownV2")

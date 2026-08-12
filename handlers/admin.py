from aiogram import Router, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from config import ADMIN_ID

router = Router()

# In-memory user tracking (you can sync this with MongoDB/SQLite)
registered_users = set()

@router.message(Command("stats"))
async def cmd_stats(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return  # Restrict command to admin only

    stats_text = (
        "📊 *Nova\\-V2 System Metrics*\n\n"
        f"• *Total Users Registered:* `{len(registered_users)}` Users\n"
        "• *AI Engine:* Google Gemini 1\\.5 Flash\n"
        "• *Status:* 🟢 Operational"
    )
    await message.answer(stats_text, parse_mode=ParseMode.MARKDOWN_V2)


@router.message(Command("broadcast"))
async def cmd_broadcast(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    # Check if the broadcast command is a reply to a media post or caption message
    if not message.reply_to_message:
        await message.answer(
            "⚠️ **How to Broadcast Media:**\n\n"
            "1. Send or upload your photo/video with your desired caption to this chat.\n"
            "2. **Reply** to that media message with `/broadcast`.\n\n"
            "This will broadcast the exact photo/video along with its caption to all users!"
        )
        return

    target_message = message.reply_to_message
    successful = 0
    failed = 0

    await message.answer(f"📢 Starting media broadcast to `{len(registered_users)}` users...")

    for user_id in registered_users:
        try:
            # copy_message automatically duplicates photo, video, document, and caption perfectly
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
    await message.answer(summary, parse_mode=ParseMode.MARKDOWN_V2)
  

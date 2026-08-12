import io
from aiogram import Router, F, types
from aiogram.enums import ParseMode
from services.gemini import generate_response
from handlers.formatter import format_telegram_md

router = Router()

@router.message(F.photo)
async def handle_photo(message: types.Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    # Download highest resolution photo
    photo = message.photo[-1]
    photo_file = await message.bot.get_file(photo.file_id)
    photo_bytes = await message.bot.download_file(photo_file.file_path)

    # Use caption if provided, otherwise default to image analysis prompt
    prompt = message.caption if message.caption else (
        "Analyze this image in detail. If it shows a product, extract its details, "
        "specs, and write an attractive product description for social media posting."
    )

    # Send to Gemini vision model
    response_text = await generate_response(prompt=prompt, image_bytes=photo_bytes.read())
    formatted_response = format_telegram_md(response_text)

    try:
        await message.answer(formatted_response, parse_mode=ParseMode.MARKDOWN_V2)
    except Exception:
        await message.answer(response_text)


@router.message(F.voice)
async def handle_voice(message: types.Message):
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")

    # Inform user about voice note processing
    voice = message.voice
    voice_file = await message.bot.get_file(voice.file_id)
    voice_bytes = await message.bot.download_file(voice_file.file_path)

    prompt = "Listen to this audio clip, transcribe the user's request accurately, and provide a helpful response."
    
    # Process audio with Gemini's multimodal audio handling
    response_text = await generate_response(prompt=prompt, image_bytes=voice_bytes.read())
    formatted_response = format_telegram_md(response_text)

    try:
        await message.answer(formatted_response, parse_mode=ParseMode.MARKDOWN_V2)
    except Exception:
        await message.answer(response_text)
      

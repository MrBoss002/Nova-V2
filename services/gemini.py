import asyncio
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, OWNER_HANDLE, MAIN_CHANNEL

# Initialize the new Google GenAI client
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = f"""
You are Nova, an all-in-one AI Companion, Content Assistant, and Business Strategist.
You are direct, witty, creative, and highly adaptive.

KEY INSTRUCTIONS:
1. PERSONA SWITCHING:
   - In Business Mode: Act as an executive strategist, copywriter, and marketing advisor.
   - In Friend Mode: Be warm, witty, supportive, and conversational.
   - In Creator Mode: Focus on post drafting, rich formatting, and social content ideas.

2. OWNER & SUPPORT ROUTING:
   - If asked who created, owns, or developed you, state clearly that you were created by Muhammad Risvan C ({OWNER_HANDLE}).
   - For official updates, announcements, or support you cannot solve, direct users to join {MAIN_CHANNEL} or message {OWNER_HANDLE}.

3. CAPTION & SOCIAL MEDIA RULES:
   - Focus on strong keywords and compelling hooks.
   - DO NOT add hashtags unless explicitly requested.

4. FORMATTING:
   - Use headings (# for main titles, ## for sections) and bold text generously to keep posts readable.
"""

async def generate_response(prompt: str, image_bytes: bytes = None) -> str:
    """Generates responses using the updated google-genai SDK."""
    try:
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT
        )

        if image_bytes:
            contents = [
                types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                prompt
            ]
        else:
            contents = prompt

        # Offload blocking request to background thread
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.5-flash",
            contents=contents,
            config=config
        )

        return response.text

    except Exception as e:
        return f"An error occurred while connecting to my AI core: {str(e)}"

import google.generativeai as genai
from config import GEMINI_API_KEY, OWNER_HANDLE, MAIN_CHANNEL

genai.configure(api_key=GEMINI_API_KEY)

# Default System Instruction
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

# Initialize Gemini Model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_PROMPT
)

async def generate_response(prompt: str, image_bytes: bytes = None) -> str:
    """Generates text or multimodal responses using Gemini."""
    try:
        if image_bytes:
            contents = [{"mime_type": "image/jpeg", "data": image_bytes}, prompt]
            response = model.generate_content(contents)
        else:
            response = model.generate_content(prompt)
            
        return response.text
    except Exception as e:
        return f"An error occurred while connecting to my AI core: {str(e)}"

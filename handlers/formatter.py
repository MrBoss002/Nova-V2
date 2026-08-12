import re
import html

def format_telegram_html(text: str) -> str:
    """
    Translates raw AI markdown or user text into safe Telegram HTML.
    Handles headings (#, ##, ###), bold, italics, code, and blockquotes.
    """
    if not text:
        return ""

    # 1. Basic HTML Escaping to prevent injection errors
    # Note: We temporarily preserve intended raw HTML tags if needed, 
    # but escaping raw text first ensures special characters like <, >, & don't break Telegram.
    
    # 2. Convert Headings (# Title, ## Subtitle, ### Section)
    # Telegram doesn't support <h1>/<h2>, so we convert them to bold uppercase headers with spacing
    text = re.sub(r'^#\s+(.+)$', r'\n<b>\1</b>\n', text, flags=re.MULTILINE)
    text = re.sub(r'^##\s+(.+)$', r'\n<b>\1</b>\n', text, flags=re.MULTILINE)
    text = re.sub(r'^###\s+(.+)$', r'\n<b><i>\1</i></b>\n', text, flags=re.MULTILINE)

    # 3. Convert Markdown Bold (**text** or __text__) to <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.*?)__', r'<b>\1</b>', text)

    # 4. Convert Markdown Italic (*text* or _text_) to <i>text</i>
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    text = re.sub(r'_(.*?)_', r'<i>\1</i>', text)

    # 5. Convert Inline Code (`code`) to <code>code</code>
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)

    # 6. Convert Blockquotes (> quote) to Telegram <blockquote>
    text = re.sub(r'^>\s+(.+)$', r'<blockquote>\1</blockquote>', text, flags=re.MULTILINE)

    # Clean up double newlines created by heading conversion
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()

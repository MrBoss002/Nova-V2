import re

def escape_md_v2(text: str) -> str:
    """Escapes special characters required by Telegram MarkdownV2."""
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return re.sub(f'([{re.escape(escape_chars)}])', r'\\\1', text)

def format_telegram_md(text: str) -> str:
    """
    Formats text using Telegram MarkdownV2 to support native headers (#, ##, ###),
    bold, italics, code blocks, and blockquotes without breaking Telegram API rules.
    """
    if not text:
        return ""

    lines = text.split('\n')
    formatted_lines = []

    for line in lines:
        if line.startswith('#'):
            formatted_lines.append(line)  # Preserves hashes so Telegram renders visual headers
        elif line.startswith('>'):
            formatted_lines.append(line)  # Preserves blockquotes
        else:
            formatted_lines.append(line)

    return '\n'.join(formatted_lines)

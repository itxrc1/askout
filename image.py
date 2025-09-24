import pathlib
import tempfile
import uuid
import imgkit
import re

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Generate PNG</title>
    <!-- Google Fonts: Poppins -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Poppins', sans-serif;
            background: transparent;
        }}
        .container {{
            width: 1200px;
            margin: 0 auto;
            padding: 72px;
            background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 50%, #e0e7ff 100%);
        }}
        .message-card {{
            background: rgba(255, 255, 255, 0.9);
            border-radius: 40px;
            padding: 72px;
            box-shadow: 0 40px 50px -10px rgba(0, 0, 0, 0.08);
            backdrop-filter: blur(10px);
        }}
        .header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 48px;
        }}
        .sender {{
            background: linear-gradient(135deg, #3b82f6, #6366f1);
            color: white;
            padding: 20px 40px;
            border-radius: 28px;
            font-size: 32px;
            font-weight: 600;
        }}
        .timestamp {{
            background: #f1f5f9;
            color: #64748b;
            padding: 12px 28px;
            border-radius: 28px;
            font-size: 26px;
            font-weight: 500;
        }}
        .message-content-wrapper {{
            position: relative;
        }}
        .message-gradient {{
            position: absolute;
            left: 0;
            top: 0;
            width: 10px;
            height: 100%;
            background: linear-gradient(to bottom, #3b82f6, #6366f1);
            border-radius: 5px;
        }}
        .message-content {{
            padding-left: 56px;
            color: #334155;
            line-height: 2.1;
            font-weight: 500;
            font-size: 44px;
            word-break: break-word;
        }}
        .emoji {{
            height: 1em;
            width: 1em;
            vertical-align: -0.1em;
        }}
    </style>
</head>
<body>
    <div class="container" id="message-card">
        <div class="message-card">
            <div class="header">
                <div class="sender">{sender}</div>
                <div class="timestamp">{timestamp}</div>
            </div>
            <div class="message-content-wrapper">
                <div class="message-gradient"></div>
                <div class="message-content">{message}</div>
            </div>
        </div>
    </div>
</body>
</html>
"""

def replace_emojis_with_twemoji(text: str) -> str:
    def emoji_to_img(match):
        char = match.group(0)
        codepoint = "-".join(f"{ord(c):x}" for c in char)
        url = f"https://twemoji.maxcdn.com/v/latest/svg/{codepoint}.svg"
        return f'<img src="{url}" alt="{char}" class="emoji">'
    
    # Match most emoji ranges
    emoji_pattern = re.compile(
        r"[\U0001F600-\U0001F64F"  # emoticons
        r"\U0001F300-\U0001F5FF"   # symbols & pictographs
        r"\U0001F680-\U0001F6FF"   # transport & map
        r"\U0001F1E0-\U0001F1FF"   # flags
        r"\U00002700-\U000027BF"   # dingbats
        r"\U0001F900-\U0001F9FF"   # supplemental symbols
        r"\U00002600-\U000026FF"   # misc symbols
        r"]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(emoji_to_img, text)

def generate_message_image(text: str, name: str = "Anonymous", compact: bool = True) -> str:
    sender = name if (name and isinstance(name, str)) else "Anonymous"
    timestamp = "Just now"

    # Replace emojis with Twemoji <img>
    message_with_emojis = replace_emojis_with_twemoji(text.replace("\n", "<br>"))

    html_content = HTML_TEMPLATE.format(
        sender=sender,
        timestamp=timestamp,
        message=message_with_emojis
    )

    temp_dir = tempfile.gettempdir()
    file_id = uuid.uuid4().hex
    html_path = pathlib.Path(temp_dir) / f"msg_{file_id}.html"
    png_path = pathlib.Path(temp_dir) / f"msg_{file_id}.png"
    html_path.write_text(html_content, encoding="utf-8")

    options = {
        "format": "png",
        "width": "1200",   # matches the HTML container width
        "encoding": "UTF-8",
        "quiet": "",
    }

    try:
        imgkit.from_file(str(html_path), str(png_path), options=options)
        if not png_path.exists() or png_path.stat().st_size == 0:
            print("❌ Image generation failed: Output PNG not created.")
            return None
        return str(png_path)
    except Exception as ex:
        print(f"❌ Image generation failed: {ex}")
        return None
    finally:
        try:
            html_path.unlink(missing_ok=True)
        except Exception:
            pass

# Example usage:
# img = generate_message_image("Hello 😃👍🏼🚀", "Copilot")
# print(img)

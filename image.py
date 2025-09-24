import pathlib
import tempfile
import uuid
import imgkit
import re  # Added re module for regex processing

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Message Card</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <script src="https://twemoji.maxcdn.com/v/latest/twemoji.min.js" crossorigin="anonymous"></script>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: #f5f5f5;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .container {{
            width: 600px;
            padding: 40px;
            background: #f5f5f5;
        }}
        .message-card {{
            background: white;
            border: 1.5px solid #e8a298;
            border-radius: 20px;
            padding: 32px;
            position: relative;
            box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        }}
        .header {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            margin-bottom: 24px;
        }}
        .user-info {{
            display: flex;
            flex-direction: column;
        }}
        .sender {{
            color: #1a1a1a;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 2px;
        }}
        .bot-username {{
            color: #4a9eff;
            font-size: 14px;
            font-weight: 400;
        }}
        .menu-dots {{
            color: #666;
            font-size: 18px;
            font-weight: bold;
            line-height: 1;
        }}
        .message-content {{
            color: #1a1a1a;
            line-height: 1.6;
            font-weight: 400;
            font-size: 16px;
            word-break: break-word;
            margin-bottom: 16px;
        }}
        .message-content .hashtag,
        .message-content .username,
        .message-content .link {{
            color: #4a9eff;
            text-decoration: none;
        }}
        .heart-icon {{
            position: absolute;
            bottom: -12px;
            right: 24px;
            width: 36px;
            height: 36px;
            background: #ff4757;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 18px;
            box-shadow: 0 2px 8px rgba(255, 71, 87, 0.3);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="message-card">
            <div class="header">
                <div class="user-info">
                    <div class="sender">{sender}</div>
                    <div class="bot-username">@askoutbot</div>
                </div>
                <div class="menu-dots">•••</div>
            </div>
            <div class="message-content">{message}</div>
            <div class="heart-icon">♥</div>
        </div>
    </div>
    <script>
        twemoji.parse(document.body);
    </script>
</body>
</html>
"""

def generate_message_image(text: str, name: str = "Anonymous") -> str:
    sender = name if (name and isinstance(name, str)) else "Anonymous"
    
    processed_message = text.replace("\n", "<br>")
    # Make hashtags blue
    processed_message = re.sub(r'(#\w+)', r'<span class="hashtag">\1</span>', processed_message)
    # Make usernames blue  
    processed_message = re.sub(r'(@\w+)', r'<span class="username">\1</span>', processed_message)
    # Make URLs blue (basic pattern)
    processed_message = re.sub(r'(https?://[^\s]+)', r'<span class="link">\1</span>', processed_message)
    
    html_content = HTML_TEMPLATE.format(
        sender=sender,
        message=processed_message
    )

    temp_dir = tempfile.gettempdir()
    file_id = uuid.uuid4().hex
    html_path = pathlib.Path(temp_dir) / f"msg_{file_id}.html"
    png_path = pathlib.Path(temp_dir) / f"msg_{file_id}.png"
    html_path.write_text(html_content, encoding="utf-8")

    options = {
        "format": "png",
        "width": "600",
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

if __name__ == "__main__":
    img = generate_message_image("Hello 😃🔥✨🚀 This looks strong & modern!", "Copilot")
    print("Generated image path:", img)

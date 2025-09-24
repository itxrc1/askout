import pathlib
import tempfile
import uuid
import imgkit

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Message Card</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
            background: #0a0a0a;
        }}
        .container {{
            width: 1200px;
            margin: 0 auto;
            padding: 48px;
            background: #0a0a0a;
        }}
        .message-card {{
            background: #111111;
            border: 1px solid #1e1e1e;
            border-radius: 16px;
            padding: 32px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }}
        .header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid #1e1e1e;
        }}
        .sender {{
            background: #ffffff;
            color: #000000;
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .timestamp {{
            background: #1e1e1e;
            color: #888888;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 500;
        }}
        .message-content-wrapper {{
            position: relative;
        }}
        .message-indicator {{
            position: absolute;
            left: 0;
            top: 4px;
            width: 3px;
            height: 20px;
            background: #ffffff;
            border-radius: 2px;
        }}
        .message-content {{
            padding-left: 20px;
            color: #ffffff;
            line-height: 1.6;
            font-weight: 400;
            font-size: 18px;
            word-break: break-word;
        }}
        .bot-branding {{
            margin-top: 24px;
            padding-top: 16px;
            border-top: 1px solid #1e1e1e;
            text-align: center;
        }}
        .bot-name {{
            color: #666666;
            font-size: 11px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        img.emoji {{
            height: 1.2em;
            width: 1.2em;
            margin: 0 .05em;
            vertical-align: -0.2em;
        }}
    </style>
    <script src="https://twemoji.maxcdn.com/v/latest/twemoji.min.js" crossorigin="anonymous"></script>
</head>
<body>
    <div class="container" id="message-card">
        <div class="message-card">
            <div class="header">
                <div class="sender">{sender}</div>
                <div class="timestamp">{timestamp}</div>
            </div>
            <div class="message-content-wrapper">
                <div class="message-indicator"></div>
                <div class="message-content">{message}</div>
            </div>
            <div class="bot-branding">
                <div class="bot-name">Askout Bot</div>
            </div>
        </div>
    </div>
    <script>
      document.addEventListener("DOMContentLoaded", function() {{
          twemoji.parse(document.body, {{folder: "svg", ext: ".svg"}});
      }});
    </script>
</body>
</html>
"""

def generate_message_image(text: str, name: str = "Anonymous") -> str:
    sender = name if (name and isinstance(name, str)) else "Anonymous"
    timestamp = "Just now"

    html_content = HTML_TEMPLATE.format(
        sender=sender,
        timestamp=timestamp,
        message=text.replace("\n", "<br>")
    )

    temp_dir = tempfile.gettempdir()
    file_id = uuid.uuid4().hex
    html_path = pathlib.Path(temp_dir) / f"msg_{file_id}.html"
    png_path = pathlib.Path(temp_dir) / f"msg_{file_id}.png"
    html_path.write_text(html_content, encoding="utf-8")

    options = {
        "format": "png",
        "width": "1300",
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

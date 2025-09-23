import pathlib
import tempfile
import uuid
import imgkit

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
            font-family: 'Poppins', 'Segoe UI', 'Arial', 'Noto Color Emoji', 'Apple Color Emoji', sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: transparent;
        }}
        .container {{
            width: 600px;
            padding: 32px;
            background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 50%, #e0e7ff 100%);
        }}
        .message-card {{
            background: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            padding: 32px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }}
        .header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 18px;
        }}
        .sender {{
            background: linear-gradient(135deg, #3b82f6, #6366f1);
            color: white;
            padding: 8px 16px;
            border-radius: 14px;
            font-size: 15px;
            font-weight: 600;
        }}
        .timestamp {{
            background: #f1f5f9;
            color: #64748b;
            padding: 6px 12px;
            border-radius: 14px;
            font-size: 13px;
            font-weight: 500;
        }}
        .message-content-wrapper {{
            position: relative;
        }}
        .message-gradient {{
            position: absolute;
            left: 0;
            top: 0;
            width: 5px;
            height: 100%;
            background: linear-gradient(to bottom, #3b82f6, #6366f1);
            border-radius: 3px;
        }}
        .message-content {{
            padding-left: 28px;
            color: #334155;
            line-height: 1.7;
            font-weight: 500;
            font-size: 20px;
            word-break: break-word;
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

def generate_message_image(text: str, name: str = "Anonymous", compact: bool = True) -> str:
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
        "width": "1200",      # double width for higher DPI
        "zoom": "2.0",        # render at 2x for better quality
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
# img = generate_message_image("Test 😃", "Copilot")
# print(img)

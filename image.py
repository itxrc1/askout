import pathlib
import tempfile
import uuid
import imgkit

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Message Card</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Poppins', sans-serif;
            background: #0a0a0a;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .container {{
            width: 1200px;
            padding: 40px;
            background: linear-gradient(135deg, #1a1a1a 0%, #2d1b69 50%, #1a1a1a 100%);
            position: relative;
            overflow: hidden;
        }}
        .container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.2) 0%, transparent 50%);
            pointer-events: none;
        }}
        .message-card {{
            background: rgba(15, 15, 15, 0.95);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 24px;
            padding: 48px;
            position: relative;
            backdrop-filter: blur(20px);
            box-shadow: 
                0 20px 40px rgba(0, 0, 0, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }}
        .header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 32px;
            padding-bottom: 20px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .sender {{
            background: linear-gradient(135deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 12px 24px;
            border-radius: 16px;
            font-size: 24px;
            font-weight: 600;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
        }}
        .timestamp {{
            background: rgba(255, 255, 255, 0.05);
            color: rgba(255, 255, 255, 0.7);
            padding: 8px 16px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 500;
            font-family: 'JetBrains Mono', monospace;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .message-content {{
            color: #ffffff;
            line-height: 1.6;
            font-weight: 400;
            font-size: 32px;
            word-break: break-word;
            position: relative;
            padding: 24px;
            background: rgba(255, 255, 255, 0.02);
            border-radius: 16px;
            border-left: 4px solid #ff6b6b;
            margin-top: 8px;
        }}
        .message-content::before {{
            content: '"';
            position: absolute;
            top: -10px;
            left: 16px;
            font-size: 60px;
            color: rgba(255, 107, 107, 0.3);
            font-family: serif;
            line-height: 1;
        }}
        .message-content::after {{
            content: '"';
            position: absolute;
            bottom: -30px;
            right: 16px;
            font-size: 60px;
            color: rgba(255, 107, 107, 0.3);
            font-family: serif;
            line-height: 1;
        }}
        .glow-effect {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, rgba(255, 107, 107, 0.1) 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
            z-index: -1;
        }}
        img.emoji {{
            height: 1.1em;
            width: 1.1em;
            margin: 0 .05em;
            vertical-align: -0.15em;
        }}
        .corner-accent {{
            position: absolute;
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #ff6b6b, transparent);
            border-radius: 50%;
            opacity: 0.3;
        }}
        .corner-accent.top-left {{
            top: -30px;
            left: -30px;
        }}
        .corner-accent.bottom-right {{
            bottom: -30px;
            right: -30px;
            background: linear-gradient(135deg, transparent, #ee5a24);
        }}
    </style>
    <script src="https://twemoji.maxcdn.com/v/latest/twemoji.min.js" crossorigin="anonymous"></script>
</head>
<body>
    <div class="container">
        <div class="message-card">
            <div class="glow-effect"></div>
            <div class="corner-accent top-left"></div>
            <div class="corner-accent bottom-right"></div>
            <div class="header">
                <div class="sender">{sender}</div>
                <div class="timestamp">{timestamp}</div>
            </div>
            <div class="message-content">{message}</div>
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

import imgkit
from PIL import Image
import tempfile
import os

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
            background: transparent !important;
        }}
        .container {{
            width: 1200px;
            margin: 0 auto;
            padding: 64px;
            background: transparent !important;
        }}
        .message-card {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 36px;
            padding: 64px;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(16px);
        }}
        .header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 40px;
        }}
        .sender {{
            background: linear-gradient(135deg, #2563eb, #7c3aed);
            color: white;
            padding: 18px 36px;
            border-radius: 24px;
            font-size: 40px;
            font-weight: 700;
        }}
        .timestamp {{
            background: #f1f5f9;
            color: #475569;
            padding: 12px 28px;
            border-radius: 20px;
            font-size: 22px;
            font-weight: 500;
        }}
        .message-content-wrapper {{
            position: relative;
        }}
        .message-gradient {{
            position: absolute;
            left: 0;
            top: 0;
            width: 8px;
            height: 100%;
            background: linear-gradient(to bottom, #2563eb, #7c3aed);
            border-radius: 4px;
        }}
        .message-content {{
            padding-left: 48px;
            color: #1e293b;
            line-height: 1.9;
            font-weight: 500;
            font-size: 46px;
            word-break: break-word;
        }}
        img.emoji {{
            height: 1.1em;
            width: 1.1em;
            margin: 0 .05em;
            vertical-align: -0.15em;
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
                <div class="message-gradient"></div>
                <div class="message-content">{message}</div>
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

def generate_message_card(sender, timestamp, message, output_path="message.png"):
    # Fill template
    html_content = HTML_TEMPLATE.format(sender=sender, timestamp=timestamp, message=message)

    # Save HTML to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as f:
        f.write(html_content.encode("utf-8"))
        temp_html = f.name

    # imgkit options (transparent background)
    options = {
        "format": "png",
        "width": "1300",
        "encoding": "UTF-8",
        "quiet": "",
        "transparent": ""
    }

    temp_png = tempfile.NamedTemporaryFile(delete=False, suffix=".png").name

    # Render HTML to PNG
    imgkit.from_file(temp_html, temp_png, options=options)

    # Open PNG and auto-trim transparent edges
    img = Image.open(temp_png).convert("RGBA")
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    img.save(output_path)

    # Cleanup
    os.remove(temp_html)
    os.remove(temp_png)

    print(f"✅ Card saved at {output_path}")

# Example usage
if __name__ == "__main__":
    generate_message_card(
        sender="Syed Tahseen",
        timestamp="2025-09-24 12:45",
        message="Hello 👋 This is a test message with emojis 😊🔥🚀",
        output_path="final_card.png"
    )

import imgkit
import tempfile
import os

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Message Card</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
            background: transparent !important;
        }
        .card {
            display: inline-block;
            padding: 40px;
            border-radius: 28px;
            font-size: 40px;
            font-weight: 500;
            line-height: 1.6;
            color: #1e293b;
            max-width: 1100px;
            word-wrap: break-word;
            box-shadow: 0 8px 24px rgba(0,0,0,0.15);
            background: #ffffff;
        }
        .sender {
            font-weight: 700;
            font-size: 44px;
            margin-bottom: 18px;
            color: #111827;
        }
        .timestamp {
            font-size: 22px;
            color: #6b7280;
            margin-top: 20px;
            text-align: right;
        }
        .emoji {
            font-family: 'Twemoji Mozilla', 'Apple Color Emoji', 'Segoe UI Emoji', 'Noto Color Emoji', sans-serif;
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="sender">{sender}</div>
        <div class="message-content">{message}</div>
        <div class="timestamp">{timestamp}</div>
    </div>
</body>
</html>
"""

def generate_message_image(sender: str, timestamp: str, message: str, output_path: str = "message.png") -> str:
    """
    Generate a styled message card image with transparent background.
    """
    html_content = HTML_TEMPLATE.format(
        sender=sender,
        message=message,
        timestamp=timestamp
    )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        tmp_file.write(html_content.encode("utf-8"))
        tmp_file_path = tmp_file.name

    options = {
        "format": "png",
        "encoding": "UTF-8",
        "quiet": "",
        "transparent": ""  # transparent background
    }

    try:
        imgkit.from_file(tmp_file_path, output_path, options=options)
    finally:
        os.remove(tmp_file_path)

    return output_path

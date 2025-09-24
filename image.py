import pathlib
import tempfile
import uuid
import imgkit

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Askout Message Card</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            color-scheme: light;
        }}
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
            background: transparent;
        }}
        .canvas {{
            width: 1200px;
            margin: 0 auto;
            padding: 80px 88px;
            background: #F8FAFC;
            box-sizing: border-box;
        }}
        .message-card {{
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 40px;
            box-shadow: 0 30px 70px rgba(15, 23, 42, 0.12);
            padding: 64px 72px;
            display: flex;
            flex-direction: column;
            gap: 48px;
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 32px;
        }}
        .sender {{
            display: flex;
            align-items: center;
            gap: 28px;
        }}
        .sender-avatar {{
            flex-shrink: 0;
            width: 88px;
            height: 88px;
            border-radius: 50%;
            background: #2563EB;
            color: #FFFFFF;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 44px;
            font-weight: 700;
        }}
        .sender-details {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        .sender-name {{
            font-size: 44px;
            font-weight: 700;
            color: #0F172A;
            letter-spacing: -0.02em;
        }}
        .timestamp {{
            padding: 14px 32px;
            border-radius: 999px;
            border: 1px solid #E2E8F0;
            font-size: 24px;
            font-weight: 500;
            color: rgba(15, 23, 42, 0.7);
            background: rgba(37, 99, 235, 0.08);
        }}
        .message-body {{
            position: relative;
            padding-left: 40px;
            border-left: 6px solid #2563EB;
        }}
        .message-body::before {{
            content: "“";
            position: absolute;
            top: -32px;
            left: -24px;
            font-size: 110px;
            font-weight: 600;
            color: rgba(37, 99, 235, 0.18);
        }}
        .message-text {{
            font-size: 46px;
            line-height: 1.7;
            font-weight: 500;
            color: #0F172A;
            word-break: break-word;
        }}
        .footer {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-top: 1px solid #E2E8F0;
            padding-top: 32px;
        }}
        .footer-brand {{
            display: flex;
            align-items: center;
            gap: 16px;
            font-size: 24px;
            font-weight: 600;
            color: #0F172A;
        }}
        .footer-brand span {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: #2563EB;
            color: #FFFFFF;
            font-size: 24px;
            font-weight: 700;
        }}
        .footer-tagline {{
            font-size: 24px;
            font-weight: 500;
            color: rgba(15, 23, 42, 0.6);
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
    <div class="canvas">
        <article class="message-card" aria-labelledby="sender-name">
            <header class="card-header">
                <div class="sender">
                    <div class="sender-avatar" aria-hidden="true">{sender_initial}</div>
                    <div class="sender-details">
                        <div class="sender-name" id="sender-name">{sender}</div>
                        <div class="footer-tagline">Anonymous message delivered</div>
                    </div>
                </div>
                <div class="timestamp">{timestamp}</div>
            </header>
            <div class="message-body">
                <div class="message-text">{message}</div>
            </div>
            <footer class="footer">
                <div class="footer-brand">
                    <span>A</span>
                    Askout Bot
                </div>
                <div class="footer-tagline">Say it freely. We'll keep it anonymous.</div>
            </footer>
        </article>
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
    sender_clean = sender.strip()
    sender_initial = sender_clean[:1].upper() if sender_clean else "A"

    html_content = HTML_TEMPLATE.format(
        sender=sender,
        sender_initial=sender_initial,
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

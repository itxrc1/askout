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
            background: linear-gradient(160deg, #0ea5e9 0%, #0369a1 100%);
        }}
        .canvas {{
            width: 1200px;
            margin: 0 auto;
            padding: 80px 0;
        }}
        .message-card {{
            position: relative;
            max-width: 860px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 24px;
            padding: 60px 72px 76px;
            box-shadow: 0 35px 70px rgba(3, 54, 94, 0.28);
        }}
        .message-card::after {{
            content: "";
            position: absolute;
            left: 50%;
            bottom: -28px;
            transform: translateX(-50%) rotate(45deg);
            width: 56px;
            height: 56px;
            background: #ffffff;
            box-shadow: 12px 12px 30px rgba(3, 54, 94, 0.18);
        }}
        .message-title {{
            margin: 0;
            font-size: 54px;
            font-weight: 700;
            color: #0f172a;
            text-align: center;
        }}
        .message-divider {{
            width: 100%;
            height: 1px;
            background: #e2e8f0;
            margin: 34px 0;
        }}
        .message-body {{
            margin: 0;
            font-size: 34px;
            line-height: 1.6;
            color: #334155;
            text-align: center;
            word-break: break-word;
        }}
        .message-meta {{
            margin-top: 26px;
            font-size: 24px;
            color: #94a3b8;
            text-align: center;
            font-weight: 500;
        }}
        .message-stars {{
            margin-top: 42px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 14px;
        }}
        .message-stars span {{
            font-size: 42px;
            color: #f59e0b;
        }}
        img.emoji {{
            height: 1.15em;
            width: 1.15em;
            margin: 0 .05em;
            vertical-align: -0.18em;
        }}
    </style>
    <script src="https://twemoji.maxcdn.com/v/latest/twemoji.min.js" crossorigin="anonymous"></script>
</head>
<body>
    <div class="canvas" id="message-card">
        <div class="message-card">
            <h1 class="message-title">{sender}</h1>
            <div class="message-divider"></div>
            <p class="message-body">{message}</p>
            <div class="message-meta">{timestamp}</div>
            <div class="message-stars">
                <span>★</span>
                <span>★</span>
                <span>★</span>
                <span>★</span>
                <span>★</span>
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

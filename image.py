import pathlib
import tempfile
import uuid
import imgkit
import re

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Askout Message Card</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            color-scheme: light;
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --card-bg: #ffffff;
            --surface-bg: #f8fafc;
            --text-primary: #0f172a;
            --text-secondary: #64748b;
            --accent-color: #3b82f6;
            --border-color: #e2e8f0;
            --shadow-color: rgba(15, 23, 42, 0.08);
            --heart-bg: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        }}
        * {{
            box-sizing: border-box;
        }}
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--surface-bg);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        .stage {{
            position: relative;
            width: 1200px;
            padding: 80px 60px 100px;
            background: var(--surface-bg);
            border-radius: 32px;
        }}
        .stage::before {{
            content: "";
            position: absolute;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            width: 140px;
            height: 6px;
            border-radius: 999px;
            background: var(--primary-gradient);
            opacity: 0.6;
        }}
        .card {{
            position: relative;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 24px;
            padding: 60px 64px 80px;
            display: flex;
            flex-direction: column;
            gap: 40px;
            box-shadow: 
                0 20px 25px -5px var(--shadow-color),
                0 10px 10px -5px rgba(15, 23, 42, 0.04),
                0 0 0 1px rgba(15, 23, 42, 0.05);
            backdrop-filter: blur(10px);
        }}
        .card::before {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--primary-gradient);
            border-radius: 24px 24px 0 0;
        }}
        .profile {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 32px;
        }}
        .profile-left {{
            display: flex;
            align-items: center;
            gap: 24px;
        }}
        .avatar {{
            width: 64px;
            height: 64px;
            border-radius: 50%;
            background: var(--primary-gradient);
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Space Grotesk', sans-serif;
            font-size: 24px;
            font-weight: 700;
            color: white;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        .profile-meta {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .sender-name {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 36px;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.02em;
            text-wrap: balance;
            line-height: 1.1;
        }}
        .sender-handle {{
            font-size: 20px;
            font-weight: 500;
            color: var(--accent-color);
            opacity: 0.8;
        }}
        .menu-dots {{
            display: flex;
            flex-direction: row;
            gap: 8px;
            margin-top: 8px;
        }}
        .menu-dots span {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--text-secondary);
            opacity: 0.4;
        }}
        .message {{
            font-size: 32px;
            line-height: 1.6;
            color: var(--text-primary);
            font-weight: 500;
            word-break: break-word;
            letter-spacing: -0.01em;
        }}
        .profile + .message {{
            margin-top: 16px;
        }}
        .message .hashtag {{
            color: var(--accent-color);
            font-weight: 600;
            background: rgba(59, 130, 246, 0.1);
            padding: 2px 8px;
            border-radius: 8px;
            text-decoration: none;
        }}
        .heart-badge {{
            position: absolute;
            right: 64px;
            bottom: -32px;
            width: 80px;
            height: 80px;
            border-radius: 50%;
            background: var(--heart-bg);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 
                0 20px 25px -5px rgba(245, 87, 108, 0.25),
                0 10px 10px -5px rgba(245, 87, 108, 0.1);
            border: 3px solid var(--card-bg);
        }}
        .heart-badge svg {{
            width: 32px;
            height: 32px;
            fill: #ffffff;
            filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
        }}
        .heart-badge::before {{
            content: "";
            position: absolute;
            inset: -2px;
            border-radius: 50%;
            background: var(--heart-bg);
            z-index: -1;
            opacity: 0.3;
            filter: blur(8px);
        }}
        img.emoji {{
            height: 1.1em;
            width: 1.1em;
            margin: 0 .05em;
            vertical-align: -0.15em;
        }}
        .timestamp {{
            position: absolute;
            top: 24px;
            right: 24px;
            font-size: 14px;
            color: var(--text-secondary);
            opacity: 0.6;
            font-weight: 500;
        }}
    </style>
    <script src="https://twemoji.maxcdn.com/v/latest/twemoji.min.js" crossorigin="anonymous"></script>
</head>
<body>
    <div class="stage" role="presentation">
        <article class="card" aria-labelledby="sender-name">
            <div class="timestamp">Just now</div>
            <header class="profile">
                <div class="profile-left">
                    <div class="avatar">{sender_initial}</div>
                    <div class="profile-meta">
                        <div class="sender-name" id="sender-name">{sender}</div>
                        <div class="sender-handle">{sender_handle}</div>
                    </div>
                </div>
                <div class="menu-dots" aria-hidden="true">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </header>
            <div class="message">{message}</div>
            <div class="heart-badge" aria-hidden="true">
                <svg viewBox="0 0 24 24">
                    <path d="M12 21s-5.7-4.46-8.4-7.18C1.86 11.08 1 9.37 1 7.5 1 4.42 3.42 2 6.5 2 8.24 2 9.91 2.81 11 4.09 12.09 2.81 13.76 2 15.5 2 18.58 2 21 4.42 21 7.5c0 1.87-.86 3.58-2.6 6.32C17.7 16.54 12 21 12 21z"/>
                </svg>
            </div>
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

def generate_message_image(text: str, name: str = "Askout Bot") -> str:
    sender = name if (name and isinstance(name, str)) else "Askout Bot"
    timestamp = "Just now"
    sender_clean = sender.strip()
    sender_initial = sender_clean[:1].upper() if sender_clean else "A"
    slug_source = sender_clean if sender_clean and sender_clean.lower() != "anonymous" else "askoutbot"
    handle_slug = re.sub(r"[^a-z0-9]+", "", slug_source.lower().replace(" ", "")) or "askoutbot"
    sender_handle = f"@{handle_slug}"
    hashtagged = re.sub(r"(?<!\w)#([A-Za-z0-9_]+)", r'<span class="hashtag">#\1</span>', text)
    formatted_message = hashtagged.replace("\n", "<br>")

    html_content = HTML_TEMPLATE.format(
        sender=sender,
        sender_initial=sender_initial,
        sender_handle=sender_handle,
        timestamp=timestamp,
        message=formatted_message
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

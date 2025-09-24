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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            color-scheme: light;
        }}
        * {{
            box-sizing: border-box;
        }}
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        .stage {{
            position: relative;
            width: 1200px;
            padding: 96px 88px 120px;
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border-radius: 56px;
        }}
        .stage::before {{
            content: "";
            position: absolute;
            top: 28px;
            left: 50%;
            transform: translateX(-50%);
            width: 160px;
            height: 20px;
            border-radius: 999px;
            background: rgba(15, 23, 42, 0.08);
        }}
        .card {{
            position: relative;
            background: #FFFFFF;
            border: 3px solid #89f7fe;
            border-radius: 36px;
            display: flex;
            flex-direction: column;
            box-shadow: 0 28px 70px rgba(137, 247, 254, 0.15);
        }}
        /* Updated gradient header with holographic colors matching the reference image */
        .gradient-header {{
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 15%, #d299c2 30%, #fef9d7 45%, #89f7fe 60%, #66a6ff 75%, #c2e9fb 90%, #a8edea 100%);
            padding: 48px 76px 32px;
            position: relative;
            border-top-left-radius: 33px;
            border-top-right-radius: 33px;
        }}
        .profile {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 32px;
            margin: 0;
        }}
        .profile-left {{
            display: flex;
            align-items: center;
            gap: 28px;
        }}
        .profile-meta {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        /* Updated sender name color for gradient background */
        .sender-name {{
            font-size: 44px;
            font-weight: 700;
            color: #FFFFFF;
            letter-spacing: -0.015em;
            text-wrap: balance;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        /* Updated sender handle color for gradient background */
        .sender-handle {{
            font-size: 26px;
            font-weight: 500;
            color: rgba(255, 255, 255, 0.9);
            text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        }}
        /* Updated menu dots color for gradient background */
        .menu-dots {{
            display: flex;
            flex-direction: row;
            gap: 12px;
            margin-top: 16px;
        }}
        .menu-dots span {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.7);
        }}
        /* Added message container with separate styling */
        .message-container {{
            padding: 48px 76px 96px;
            background: #FFFFFF;
            border-bottom-left-radius: 33px;
            border-bottom-right-radius: 33px;
        }}
        .message {{
            font-size: 42px;
            line-height: 1.65;
            color: #1F2933;
            font-weight: 500;
            word-break: break-word;
            margin: 0;
        }}
        .message .hashtag {{
            color: #3A9EC7;
            font-weight: 600;
        }}
        /* Updated heart badge to match holographic theme */
        .heart-badge {{
            position: absolute;
            right: 84px;
            bottom: -38px;
            width: 96px;
            height: 96px;
            border-radius: 50%;
            background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 50%, #a8edea 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 20px 40px rgba(137, 247, 254, 0.3);
        }}
        .heart-badge svg {{
            width: 40px;
            height: 40px;
            fill: #FFFFFF;
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
    <div class="stage" role="presentation">
        <article class="card" aria-labelledby="sender-name">
            <!-- Moved profile section into gradient header -->
            <div class="gradient-header">
                <header class="profile">
                    <div class="profile-left">
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
            </div>
            <!-- Moved message into separate container -->
            <div class="message-container">
                <div class="message">{message}</div>
            </div>
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

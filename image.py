import pathlib
import tempfile
import uuid
import imgkit

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Message Card</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * {{
            box-sizing: border-box;
        }}
        
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: transparent;
            -webkit-font-smoothing: antialiased;
        }}
        
        .container {{
            width: 1200px;
            margin: 0 auto;
            padding: 80px;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            min-height: 600px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .message-card {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 0;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.1);
            max-width: 700px;
            width: 100%;
            position: relative;
            overflow: hidden;
        }}
        
        .message-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
        }}
        
        .card-header {{
            padding: 40px 40px 0 40px;
        }}
        
        .header-content {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 32px;
        }}
        
        .sender-info {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        
        .avatar {{
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }}
        
        .sender-details {{
            display: flex;
            flex-direction: column;
        }}
        
        .sender-name {{
            font-size: 20px;
            font-weight: 600;
            color: #0f172a;
            margin: 0;
            line-height: 1.2;
        }}
        
        .sender-label {{
            font-size: 12px;
            color: #64748b;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 2px;
        }}
        
        .timestamp {{
            color: #64748b;
            font-size: 14px;
            font-weight: 500;
            background: #f8fafc;
            padding: 8px 16px;
            border-radius: 20px;
            border: 1px solid #e2e8f0;
        }}
        
        .message-body {{
            padding: 0 40px 40px 40px;
        }}
        
        .message-content {{
            color: #1e293b;
            line-height: 1.6;
            font-weight: 400;
            font-size: 28px;
            word-break: break-word;
            margin: 0;
            padding: 32px;
            background: #f8fafc;
            border-radius: 16px;
            border-left: 4px solid #3b82f6;
            position: relative;
        }}
        
        .message-content::before {{
            content: '"';
            position: absolute;
            top: 8px;
            left: 16px;
            font-size: 48px;
            color: #cbd5e1;
            font-family: Georgia, serif;
            line-height: 1;
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
    <div class="container">
        <div class="message-card">
            <div class="card-header">
                <div class="header-content">
                    <div class="sender-info">
                        <div class="avatar">🎭</div>
                        <div class="sender-details">
                            <h1 class="sender-name">{sender}</h1>
                            <div class="sender-label">Anonymous Message</div>
                        </div>
                    </div>
                    <div class="timestamp">{timestamp}</div>
                </div>
            </div>
            
            <div class="message-body">
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

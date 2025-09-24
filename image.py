import pathlib
import tempfile
import uuid
import imgkit

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Message Card</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        * {{
            box-sizing: border-box;
        }}
        
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
            background: transparent;
            -webkit-font-smoothing: antialiased;
        }}
        
        .container {{
            width: 1200px;
            margin: 0 auto;
            padding: 60px;
            background: #0a0a0a;
            min-height: 600px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }}
        
        .container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.1) 0%, transparent 50%);
        }}
        
        .message-card {{
            background: #ffffff;
            border-radius: 0;
            padding: 0;
            box-shadow: 
                0 0 0 3px #000000,
                12px 12px 0 0 #000000;
            max-width: 800px;
            width: 100%;
            position: relative;
            overflow: hidden;
            border: 3px solid #000000;
        }}
        
        .accent-bar {{
            height: 8px;
            background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
            width: 100%;
        }}
        
        .card-content {{
            padding: 48px;
        }}
        
        .header {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            margin-bottom: 40px;
            gap: 24px;
        }}
        
        .sender-section {{
            flex: 1;
        }}
        
        .anonymous-label {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            font-weight: 700;
            color: #666666;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 8px;
            background: #f5f5f5;
            padding: 6px 12px;
            display: inline-block;
            border: 2px solid #000000;
        }}
        
        .sender-name {{
            font-size: 32px;
            font-weight: 700;
            color: #000000;
            margin: 0;
            line-height: 1.1;
            text-transform: uppercase;
            letter-spacing: -1px;
        }}
        
        .timestamp {{
            font-family: 'JetBrains Mono', monospace;
            color: #000000;
            font-size: 12px;
            font-weight: 500;
            background: #ffff00;
            padding: 12px 16px;
            border: 2px solid #000000;
            text-transform: uppercase;
            letter-spacing: 1px;
            white-space: nowrap;
        }}
        
        .message-wrapper {{
            position: relative;
        }}
        
        .message-content {{
            color: #000000;
            line-height: 1.4;
            font-weight: 500;
            font-size: 24px;
            word-break: break-word;
            margin: 0;
            padding: 32px;
            background: #f8f8f8;
            border: 3px solid #000000;
            position: relative;
            min-height: 120px;
            display: flex;
            align-items: center;
        }}
        
        .quote-mark {{
            position: absolute;
            top: -8px;
            left: 24px;
            background: #ffffff;
            padding: 0 8px;
            font-size: 48px;
            font-weight: 700;
            color: #000000;
            line-height: 1;
        }}
        
        .message-footer {{
            margin-top: 24px;
            display: flex;
            justify-content: flex-end;
        }}
        
        .anonymous-badge {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 10px;
            font-weight: 700;
            color: #ffffff;
            background: #000000;
            padding: 8px 16px;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            gap: 8px;
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
            <div class="accent-bar"></div>
            
            <div class="card-content">
                <div class="header">
                    <div class="sender-section">
                        <div class="anonymous-label">Anonymous</div>
                        <h1 class="sender-name">{sender}</h1>
                    </div>
                    <div class="timestamp">{timestamp}</div>
                </div>
                
                <div class="message-wrapper">
                    <div class="quote-mark">"</div>
                    <div class="message-content">{message}</div>
                </div>
                
                <div class="message-footer">
                    <div class="anonymous-badge">
                        🎭 ANONYMOUS MESSAGE
                    </div>
                </div>
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

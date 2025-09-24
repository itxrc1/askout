import pathlib
import tempfile
import uuid
import imgkit

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Message Card</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel=\"stylesheet\">
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
            -moz-osx-font-smoothing: grayscale;
        }}
        
        .container {{
            width: 1200px;
            margin: 0 auto;
            padding: 48px;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #334155 100%);
            min-height: 600px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .message-card {{
            background: rgba(255, 255, 255, 0.98);
            border-radius: 24px;
            padding: 0;
            box-shadow: 
                0 32px 64px rgba(0, 0, 0, 0.25),
                0 0 0 1px rgba(255, 255, 255, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(226, 232, 240, 0.2);
            overflow: hidden;
            max-width: 900px;
            width: 100%;
        }}
        
        .card-header {{
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
            padding: 32px 48px;
            position: relative;
            overflow: hidden;
        }}
        
        .card-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.15"/><circle cx="20" cy="80" r="0.5" fill="white" opacity="0.15"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            opacity: 0.3;
        }}
        
        .header-content {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: relative;
            z-index: 1;
        }}
        
        .sender {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}
        
        .sender-avatar {{
            width: 56px;
            height: 56px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: 700;
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.3);
        }}
        
        .sender-info {{
            color: white;
        }}
        
        .sender-name {{
            font-size: 32px;
            font-weight: 700;
            margin: 0;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        .sender-label {{
            font-size: 16px;
            opacity: 0.9;
            margin: 4px 0 0 0;
            font-weight: 500;
        }}
        
        .timestamp {{
            background: rgba(255, 255, 255, 0.15);
            color: white;
            padding: 12px 24px;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 500;
            font-family: 'JetBrains Mono', monospace;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        
        .message-body {{
            padding: 48px;
            position: relative;
        }}
        
        .message-content {{
            color: #1e293b;
            line-height: 1.7;
            font-weight: 500;
            font-size: 36px;
            word-break: break-word;
            position: relative;
            padding: 32px;
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border-radius: 16px;
            border-left: 6px solid #3b82f6;
            box-shadow: 
                0 4px 6px rgba(0, 0, 0, 0.05),
                0 1px 3px rgba(0, 0, 0, 0.1);
        }}
        
        .message-content::before {{
            content: '"';
            position: absolute;
            top: -8px;
            left: 16px;
            font-size: 72px;
            color: #3b82f6;
            opacity: 0.3;
            font-family: Georgia, serif;
            line-height: 1;
        }}
        
        .message-footer {{
            padding: 0 48px 32px 48px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .anonymous-badge {{
            background: linear-gradient(135deg, #64748b 0%, #475569 100%);
            color: white;
            padding: 12px 24px;
            border-radius: 20px;
            font-size: 16px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }}
        
        .lock-icon {{
            width: 16px;
            height: 16px;
            opacity: 0.9;
        }}
        
        img.emoji {{
            height: 1.1em;
            width: 1.1em;
            margin: 0 .05em;
            vertical-align: -0.15em;
        }}
        
        @media (max-width: 1300px) {{
            .container {{
                width: 100%;
                padding: 32px;
            }}
            
            .message-content {{
                font-size: 32px;
            }}
            
            .sender-name {{
                font-size: 28px;
            }}
        }}
    </style>
    <script src="https://twemoji.maxcdn.com/v/latest/twemoji.min.js" crossorigin="anonymous"></script>
</head>
<body>
    <div class="container">
        <div class="message-card">
            <div class="card-header">
                <div class="header-content">
                    <div class="sender">
                        <div class="sender-avatar">
                            🎭
                        </div>
                        <div class="sender-info">
                            <h1 class="sender-name">{sender}</h1>
                            <p class="sender-label">sent you a message</p>
                        </div>
                    </div>
                    <div class="timestamp">{timestamp}</div>
                </div>
            </div>
            
            <div class="message-body">
                <div class="message-content">{message}</div>
            </div>
            
            <div class="message-footer">
                <div class="anonymous-badge">
                    <svg class="lock-icon" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd"/>
                    </svg>
                    Anonymous Message
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

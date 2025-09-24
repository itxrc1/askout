import pathlib
import tempfile
import uuid
import imgkit

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Message Card</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
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
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 700px;
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
                radial-gradient(circle at 30% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 70% 80%, rgba(255, 255, 255, 0.05) 0%, transparent 50%);
        }}
        
        .message-card {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 24px;
            padding: 0;
            box-shadow: 
                0 32px 64px rgba(0, 0, 0, 0.2),
                0 0 0 1px rgba(255, 255, 255, 0.1);
            max-width: 700px;
            width: 100%;
            position: relative;
            overflow: hidden;
        }}
        
        .card-header {{
            background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
            padding: 32px 40px 24px;
            position: relative;
        }}
        
        .card-header::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        }}
        
        .bot-info {{
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 16px;
        }}
        
        .bot-avatar {{
            width: 48px;
            height: 48px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .bot-details h3 {{
            color: white;
            font-size: 18px;
            font-weight: 600;
            margin: 0 0 4px 0;
            letter-spacing: -0.3px;
        }}
        
        .bot-details p {{
            color: rgba(255, 255, 255, 0.8);
            font-size: 14px;
            margin: 0;
            font-family: 'Fira Code', monospace;
        }}
        
        .message-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .sender-name {{
            color: white;
            font-size: 16px;
            font-weight: 500;
            background: rgba(255, 255, 255, 0.15);
            padding: 8px 16px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }}
        
        .timestamp {{
            color: rgba(255, 255, 255, 0.7);
            font-size: 13px;
            font-family: 'Fira Code', monospace;
        }}
        
        .card-content {{
            padding: 40px;
        }}
        
        .message-content {{
            color: #2d3748;
            line-height: 1.6;
            font-weight: 400;
            font-size: 20px;
            word-break: break-word;
            margin: 0;
            position: relative;
            min-height: 80px;
            display: flex;
            align-items: center;
        }}
        
        .message-content::before {{
            content: '"';
            position: absolute;
            top: -20px;
            left: -10px;
            font-size: 80px;
            color: #e2e8f0;
            font-weight: 700;
            line-height: 1;
            z-index: 0;
        }}
        
        .message-text {{
            position: relative;
            z-index: 1;
        }}
        
        .card-footer {{
            padding: 0 40px 32px;
            display: flex;
            justify-content: center;
        }}
        
        .anonymous-badge {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            gap: 8px;
            box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
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
                <div class="bot-info">
                    <div class="bot-avatar">💕</div>
                    <div class="bot-details">
                        <h3>Askout Bot</h3>
                        <p>@Askoutbot</p>
                    </div>
                </div>
                
                <div class="message-meta">
                    <div class="sender-name">From: {sender}</div>
                    <div class="timestamp">{timestamp}</div>
                </div>
            </div>
            
            <div class="card-content">
                <div class="message-content">
                    <div class="message-text">{message}</div>
                </div>
            </div>
            
            <div class="card-footer">
                <div class="anonymous-badge">
                    🎭 Anonymous Message
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

import os
import shutil
import subprocess

USB_DRIVE = "E:\\"
PROJECT_NAME = "RDX_Portable_House"
TARGET_DIR = os.path.join(USB_DRIVE, PROJECT_NAME)

def setup_portable_environment():
    print("[🚀] RDX Portable System Builder सक्रिय हो रहा है...")
    
    # 1. पेन ड्राइव में फोल्डर स्ट्रक्चर बनाना
    os.makedirs(TARGET_DIR, exist_ok=True)
    os.makedirs(os.path.join(TARGET_DIR, "modules"), exist_ok=True)
    os.makedirs(os.path.join(TARGET_DIR, "website"), exist_ok=True)
    print(f"[+] पेन ड्राइव पर बेस फोल्डर तैयार: {TARGET_DIR}")

    # 2. करंट प्रोजेक्ट फाइलों को पेन ड्राइव में शिफ्ट करना
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    for item in os.listdir(current_dir):
        s = os.path.join(current_dir, item)
        d = os.path.join(TARGET_DIR, item)
        if os.path.isdir(s):
            if item not in [".git", "__pycache__", "venv"]:
                shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    print("[+] झटका इंजन और RDX AI Studio का सारा माल पेन ड्राइव में शिफ्ट हो गया है!")

    # 3. वेबसाइट (White Page Chatbot UI) ऑटोमैटिक जेनरेट करना
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>RDX Sovereign AI Studio & Jatka Engine</title>
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: monospace; display: flex; flex-direction: column; align-items: center; justify-content: height; height: 100vh; margin: 0; }
        #chat-container { width: 600px; height: 400px; border: 1px solid #30363d; border-radius: 8px; padding: 15px; overflow-y: scroll; background: #161b22; margin-bottom: 10px; }
        .message { margin-bottom: 10px; }
        .user { color: #58a6ff; }
        .bot { color: #3fb950; }
        input { width: 500px; padding: 10px; background: #0d1117; border: 1px solid #30363d; color: #fff; border-radius: 5px; }
        button { padding: 10px 15px; background: #238636; color: #white; border: none; border-radius: 5px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>⚡ RDX Master Neural Gateway ⚡</h1>
    <div id="chat-container"></div>
    <div>
        <input type="text" id="prompt" placeholder="Ask Jatka Engine or type YouTube link for RDX Studio..." />
        <button onclick="sendQuery()">Strike</button>
    </div>

    <script>
        async function sendQuery() {
            const promptInput = document.getElementById('prompt');
            const container = document.getElementById('chat-container');
            const text = promptInput.value;
            if(!text) return;

            container.innerHTML += `<div class="message user"><b>You:</b> ${text}</div>`;
            promptInput.value = '';

            try {
                let response = await fetch('http://localhost:8001/api/v1/query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: text, user_id: "rdx_master" })
                });
                let data = await response.json();
                container.innerHTML += `<div class="message bot"><b>RDX Core:</b> ${data.response || data.message}</div>`;
            } catch(e) {
                container.innerHTML += `<div class="message bot" style="color: #f85149;">[X] Connection Error: Jatka Engine offline!</div>`;
            }
            container.scrollTop = container.scrollHeight;
        }
    </script>
</body>
</html>
"""
    web_path = os.path.join(TARGET_DIR, "website", "index.html")
    with open(web_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[+] स्मार्ट चैटबॉट वेबसाइट (UI) जनरेट हो गई: {web_path}")

    print("[✔] सारा सेटअप पेन ड्राइव में लॉक हो गया है! अब पेन ड्राइव से सीधे रन कर सकते हो। 👑")

if __name__ == "__main__":
    setup_portable_environment()
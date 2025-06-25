import os
from flask import Flask, send_from_directory
from dotenv import load_dotenv

load_dotenv()

# --- 配置 ---
# 这些值应该与 ypd.py 中的保持一致
EPISODES_DIR = os.getenv("EPISODES_DIR", "episodes")
RSS_FILE = os.getenv("RSS_FILE", "feed.xml")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

app = Flask(__name__)

@app.route('/')
def index():
    # 提供 RSS feed 文件
    return send_from_directory('.', RSS_FILE)

@app.route('/episodes/<path:filename>')
def download_episode(filename):
    # 提供音频文件
    return send_from_directory(EPISODES_DIR, filename)

def main():
    """主函数，启动服务器"""
    # 在启动服务器前，检查RSS文件是否存在
    if not os.path.exists(RSS_FILE):
        print(f"Error: RSS feed '{RSS_FILE}' not found.")
        print("Please run 'python3 ypd.py generate' to create it first.")
        return

    port = 8000
    print(f"Starting Flask server at http://localhost:{port}")
    print(f"Serving RSS feed: {BASE_URL}/{RSS_FILE}")
    print(f"Serving episodes from: ./{EPISODES_DIR}/")
    print("Press Ctrl+C to stop the server.")
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()

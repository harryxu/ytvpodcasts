import os
from flask import Flask, send_from_directory
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
# These values should be consistent with those in ypd.py
EPISODES_DIR = os.getenv("EPISODES_DIR", "episodes")
RSS_FILE = os.getenv("RSS_FILE", "feed.xml")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

app = Flask(__name__)

@app.route('/')
def index():
    # Provide the RSS feed file
    return send_from_directory('.', RSS_FILE)

@app.route('/episodes/<path:filename>')
def download_episode(filename):
    # Provide the audio files
    return send_from_directory(EPISODES_DIR, filename)

def main():
    """Main function, starts the server"""
    # Before starting the server, check if the RSS file exists
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

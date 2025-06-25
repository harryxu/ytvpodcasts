

import os
import sys
import json
import subprocess
import argparse
from datetime import datetime
from feedgen.feed import FeedGenerator
from dotenv import load_dotenv

load_dotenv()

# --- 配置 ---
# 重要：请将此URL更改为你的服务器的公共IP地址或域名
# RSS阅读器需要通过这个地址来访问你的音频文件
# 如果在本地测试，可以用 http://localhost:8000
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
PODCAST_TITLE = os.getenv("PODCAST_TITLE", "My YouTube Podcast")
PODCAST_DESCRIPTION = os.getenv("PODCAST_DESCRIPTION", "A podcast generated from YouTube videos.")
PODCAST_LINK = os.getenv("PODCAST_LINK", "https://github.com/your_repo") # 可以是你的项目地址

# --- 文件和目录路径 ---
EPISODES_DIR = os.getenv("EPISODES_DIR", "episodes")
PODCAST_DATA_FILE = os.getenv("PODCAST_DATA_FILE", "podcast.json")
RSS_FILE = os.getenv("RSS_FILE", "feed.xml")

def initialize_project():
    """检查并创建所需的目录和文件"""
    if not os.path.exists(EPISODES_DIR):
        print(f"Creating directory: {EPISODES_DIR}")
        os.makedirs(EPISODES_DIR)

    if not os.path.exists(PODCAST_DATA_FILE):
        print(f"Creating empty database: {PODCAST_DATA_FILE}")
        with open(PODCAST_DATA_FILE, "w") as f:
            json.dump({"episodes": []}, f, indent=4)
    
    print("Initialization complete.")

def get_video_info(youtube_url):
    """使用 yt-dlp 获取视频的元数据"""
    print(f"Fetching metadata for {youtube_url}...")
    command = [
        "yt-dlp",
        "--dump-json",
        youtube_url
    ]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error fetching video info: {e.stderr}")
        return None
    except FileNotFoundError:
        print("Error: 'yt-dlp' command not found.")
        print("Please install yt-dlp: pip install yt-dlp")
        sys.exit(1)


def download_audio(youtube_url):
    """下载最佳质量的音频并保存到 episodes 目录"""
    print(f"Starting audio download for {youtube_url}...")
    output_template = os.path.join(EPISODES_DIR, "%(id)s.%(ext)s")
    command = [
        "yt-dlp",
        "-f", "bestaudio[ext=m4a]", # 下载m4a格式的最佳音频
        "-o", output_template,
        youtube_url
    ]
    try:
        subprocess.run(command, check=True)
        print("Download completed successfully.")
        # 获取实际下载的文件名
        info = get_video_info(youtube_url) # 再次获取信息以确认文件名
        if info:
            filename = f"{info['id']}.m4a"
            return os.path.join(EPISODES_DIR, filename)
    except subprocess.CalledProcessError as e:
        print(f"Error downloading audio: {e}")
        return None
    except FileNotFoundError:
        print("Error: 'yt-dlp' command not found.")
        print("Please install yt-dlp: pip install yt-dlp")
        sys.exit(1)
    return None


def generate_rss():
    """从 podcast.json 生成 feed.xml"""
    print("Generating RSS feed...")
    with open(PODCAST_DATA_FILE, "r") as f:
        data = json.load(f)

    fg = FeedGenerator()
    fg.title(PODCAST_TITLE)
    fg.link(href=BASE_URL, rel="alternate")
    fg.description(PODCAST_DESCRIPTION)
    fg.language("en") # 你可以根据需要更改语言

    for episode_info in sorted(data["episodes"], key=lambda x: x["upload_date"], reverse=True):
        fe = fg.add_entry()
        fe.id(episode_info["webpage_url"])
        fe.title(episode_info["title"])
        fe.description(episode_info["description"])
        
        # 解析日期
        pub_date = datetime.strptime(episode_info["upload_date"], "%Y%m%d").strftime("%a, %d %b %Y %H:%M:%S %z")
        fe.published(pub_date + " +0000")

        # 音频文件信息
        audio_url = f"{BASE_URL}/{episode_info['audio_file']}"
        file_size = str(os.path.getsize(episode_info["audio_file"]))
        fe.enclosure(url=audio_url, length=file_size, type="audio/x-m4a")

    fg.rss_file(RSS_FILE, pretty=True)
    print(f"RSS feed saved to {RSS_FILE}")


def add_episode(youtube_url):
    """处理 'add' 命令：下载、更新数据库、重新生成RSS"""
    initialize_project()
    
    # 1. 获取视频信息
    info = get_video_info(youtube_url)
    if not info:
        return

    # 检查视频是否已存在
    with open(PODCAST_DATA_FILE, "r") as f:
        podcast_data = json.load(f)
    
    if any(ep["id"] == info["id"] for ep in podcast_data["episodes"]):
        print(f"Video '{info['title']}' already exists in the podcast. Skipping.")
        return

    # 2. 下载音频
    audio_path = download_audio(youtube_url)
    if not audio_path:
        return

    # 3. 更新 JSON 数据库
    episode_data = {
        "id": info["id"],
        "title": info["title"],
        "description": info.get("description", "No description available."),
        "webpage_url": info["webpage_url"],
        "upload_date": info["upload_date"],
        "duration": info.get("duration"),
        "thumbnail": info.get("thumbnail"),
        "audio_file": audio_path
    }
    
    podcast_data["episodes"].append(episode_data)
    with open(PODCAST_DATA_FILE, "w") as f:
        json.dump(podcast_data, f, indent=4)
    print(f"Added '{info['title']}' to {PODCAST_DATA_FILE}")

    # 4. 重新生成 RSS
    generate_rss()

def main():
    """主函数，解析命令行参数"""
    parser = argparse.ArgumentParser(description="YouTube Podcast RSS Generator")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # 'add' 命令
    add_parser = subparsers.add_subparsers("add", help="Add a new YouTube video to the podcast")
    add_parser.add_argument("url", type=str, help="The full URL of the YouTube video")

    # 'serve' 命令
    subparsers.add_subparsers("serve", help="Instructions to run the web server")

    # 'init' 命令
    subparsers.add_subparsers("init", help="Initialize the project structure")

    # 'generate' 命令
    subparsers.add_subparsers("generate", help="Force regenerate the RSS feed from existing data")

    args = parser.parse_args()

    if args.command == "init":
        initialize_project()
    elif args.command == "add":
        add_episode(args.url)
    elif args.command == "generate":
        generate_rss()
    elif args.command == "serve":
        print("To run the web server, please use the following command:")
        print("\n    python3 webapp.py\n")

if __name__ == "__main__":
    main()

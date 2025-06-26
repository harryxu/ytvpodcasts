# YouTube to Podcast RSS Feed Generator

This project provides a simple system for generating a podcast RSS feed from YouTube videos.

## Features

- **Command-line interface:** Add new YouTube videos to the podcast feed.
- **Automatic audio download:** Downloads the audio from YouTube videos.
- **RSS feed generation:** Creates a podcast RSS feed in XML format.
- **Web service:** A Flask-based web service to host the RSS feed and audio files.

## How it works

The system consists of two main components:

1.  **`ypd.py`:** A command-line tool (using `click`) to manage the podcast. You can use it to add new YouTube videos. When you add a video, it downloads the audio and updates the podcast data.
2.  **`webapp.py`:** A Flask web application that serves the generated RSS feed (`feed.xml`) and the downloaded audio files.

## Data storage

-   `podcast.json`: Stores the metadata for the podcast episodes.
-   `feed.xml`: The generated RSS feed.
-   `episodes/`: The directory where the downloaded audio files are stored.

## Usage

### Adding a new episode

To add a new YouTube video to your podcast, run the following command:

```bash
python3 ypd.py add <YOUTUBE_URL>
```

For example:

```bash
python3 ypd.py add https://www.youtube.com/watch?v=rXa3pW2sarg
```

This will:

1.  Download the audio from the YouTube video.
2.  Add the video's information to `podcast.json`.
3.  Update the `feed.xml` RSS file.

### Running the web service

To make your podcast accessible, you need to run the web service:

```bash
python3 webapp.py
```

This will start a Flask server that serves the `feed.xml` and the audio files in the `episodes/` directory.
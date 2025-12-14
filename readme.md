# YTVPodcasts

YTVPodcasts is a work in progress self-hosted tool for turning individual YouTube videos into a private podcast feed.

## Overview

The system provides a web-based dashboard where users can submit YouTube video URLs. Once submitted, the system automatically downloads the audio from the video in the background. It then generates an RSS feed for the downloaded audio, which you can subscribe to using any standard podcast client.

## Features

- **Web Dashboard**: Simple interface to submit and manage YouTube video links.
- **Background Processing**: Download YouTube videos using [yt-dlp](https://github.com/yt-dlp/yt-dlp) and converts them to audio in the background.
- **RSS Feed Generation**: Instantly creates a podcast-compatible RSS feed for your downloaded content.
- **Self-Hosted**: Run it on your own server for privacy and control.

## Getting Started

### Development

To start the development environment, ensure you have `uv` installed, then run:

```bash
make startdev
```

This command will run database migrations and start all necessary services.

### Docker

You can also run the application using Docker:

```bash
make run-docker
```

## Comparisons

**YTVPodcasts** is designed for ad-hoc downloading of **single YouTube videos**.

If you are looking for a solution to subscribe to and automatically download entire **YouTube channels** or playlists, we recommend using [Podsync](https://github.com/mxpv/podsync).

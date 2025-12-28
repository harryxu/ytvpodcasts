# YTVPodcasts

YTVPodcasts is a work in progress self-hosted tool for turning individual videos into a private podcast feed.

## Overview

The system provides a web-based dashboard where users can submit video URLs. Once submitted, the system automatically downloads the audio from the video in the background. It then generates an RSS feed for the downloaded audio, which you can subscribe to using any standard podcast client.

## Features

- **Web Dashboard**: Simple interface to submit and manage video links.
- **Background Processing**: Download videos using [yt-dlp](https://github.com/yt-dlp/yt-dlp) and converts them to audio in the background.
- **RSS Feed Generation**: Instantly creates a podcast-compatible RSS feed for your downloaded content.
- **Self-Hosted**: Run it on your own server for privacy and control.


## Development


To start the development environment, the simplest way is to use [Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers).


```shell
# Install Dev Container CLI if you haven't already.
npm install -g @devcontainers/cli

# Starting the dev container will install all Python and Node dependencies on its initial run.
# If the setup is successful, will automatically enter the dev container shell.
make devcontainer-shell

# Run the development server in dev container shell.
make startdev
```

Access http://localhost:5180/ to view the dashboard.


## Comparisons

**YTVPodcasts** is designed for ad-hoc downloading of **single videos**.

If you are looking for a solution to subscribe to and automatically download entire **channels** or playlists, we recommend using [Podsync](https://github.com/mxpv/podsync).

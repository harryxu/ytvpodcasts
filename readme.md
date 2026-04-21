# VPodcasts

VPodcasts is a self-hosted tool for turning individual online videos into a private podcast feed.

It is built for people who regularly find useful talks, interviews, tutorials, or long-form videos online and would rather listen to them in a podcast app than keep returning to a browser or video platform. Instead of managing bookmarks, tabs, or watch-later lists, you can save a video link once and have it show up as an episode in your own RSS feed.

## When VPodcasts Is Useful

VPodcasts fits best when you want to:

- listen to video content while commuting, walking, exercising, or working
- collect one-off videos from different sources into a single personal feed
- keep access to saved audio in a private, self-hosted setup
- use your preferred podcast player for playback, queueing, and progress tracking
- build your own curated listening backlog from videos that are not part of a single channel workflow

This project is especially useful for ad-hoc and selective saving. It focuses on individual videos rather than automatically mirroring entire channels or playlists.

## Main Features

- Submit a video URL from the web dashboard and turn it into a podcast episode
- Download and process audio in the background, so videos can be added without waiting on the page
- Generate a private RSS feed that works with standard podcast apps
- Browse saved episodes in a dedicated dashboard
- Review recent download tasks and their status
- Stream saved audio directly from your self-hosted instance
- Archive or remove episodes when you want to keep the feed organized

## Typical Workflow

1. Paste a video URL into the dashboard.
2. Let VPodcasts process it in the background.
3. Open your podcast app and subscribe to the generated RSS feed.
4. Listen to saved episodes like any other podcast.

## Why Use It

VPodcasts helps bridge the gap between video discovery and audio-first consumption. Many videos are worth hearing but do not need to be watched closely. This project makes those videos easier to revisit, queue, and consume in the tools people already use for podcasts.

Because it is self-hosted, it is also a good fit for users who want more control over privacy, storage, and access to their saved listening library.

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

Access [http://localhost:5180/](http://localhost:5180/) to view the dashboard.

## Comparison

**VPodcasts** is designed for ad-hoc downloading of **single videos**.

If you are looking for a solution that continuously follows and downloads full **channels** or playlists, [Podsync](https://github.com/mxpv/podsync) may be a better fit.

FROM mcr.microsoft.com/devcontainers/python:3.13

# Remove the broken Yarn apt repository that gets added by the Node devcontainer
# feature, which causes apt-get update to fail due to a missing GPG key.
RUN rm -f /etc/apt/sources.list.d/yarn.list \
    /etc/apt/sources.list.d/yarnpkg.list \
    /usr/share/keyrings/yarnkey.gpg \
    /etc/apt/keyrings/yarn.gpg \
    2>/dev/null || true

# Install ffmpeg directly, bypassing the devcontainer feature that fails due
# to the broken Yarn apt repo signature check.
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

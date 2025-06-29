FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copy dependency files and install them
# This is done in a separate step to leverage Docker layer caching.
COPY pyproject.toml uv.lock ./
RUN uv sync 

# Copy the rest of the application files
COPY alembic.ini .
COPY alembic/ ./alembic/
COPY vpodcasts/ ./vpodcasts/
COPY manager.py .

RUN mkdir data

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

COPY docker/start.sh .
RUN chmod +x start.sh

ENTRYPOINT ["./start.sh"]

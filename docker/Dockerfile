FROM python:3.13-slim

WORKDIR /app

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Install uv, our package manager
RUN pip install uv

# Copy dependency files and install them
# This is done in a separate step to leverage Docker layer caching.
COPY pyproject.toml uv.lock ./
RUN uv install

# Copy the rest of the application files
COPY webapp.py .
COPY database.py .
COPY models.py .
COPY alembic.ini .
COPY alembic/ ./alembic/

# Create the directory for episode audio files
RUN mkdir episodes

# Command to run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "webapp:app"]

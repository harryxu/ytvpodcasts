web: uv run fastapi dev vpodcasts/webapp.py --host 0.0.0.0 --port 5080
huey: uv run huey_consumer vpodcasts.huey_tasks.huey -w 1
frontend: cd dashboard && pnpm dev

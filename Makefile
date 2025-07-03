.PHONY: docker
docker:
	docker build -f docker/Dockerfile -t vpodcasts:latest .

.PHONY: huey
huey:
	uv run huey_consumer vpodcasts.huey_tasks.huey -w 1

.PHONY: devweb
devweb:
	un run manager.py web
	
.PHONY: startdev
startdev:
	uv run manager.py web & \
	uv run huey_consumer vpodcasts.huey_tasks.huey -w 1 & \
	cd dashboard && pnpm dev & \
	wait
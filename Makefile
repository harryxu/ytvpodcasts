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
	@echo "Starting services with honcho... Press Ctrl+C to stop."
	honcho start

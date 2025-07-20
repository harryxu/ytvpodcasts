.PHONY: docker
docker:
	docker build -f docker/Dockerfile -t vpodcasts:latest .

.PHONY: dashboard
dashboard:
	cd dashboard && pnpm run build

.PHONY: all
all: dashboard docker

.PHONY: huey
huey:
	# Run huey consumer as a task queue.
	uv run huey_consumer vpodcasts.huey_tasks.huey -w 1

.PHONY: devweb
devweb:
	un run manager.py web
	
.PHONY: startdev
startdev:
	# Run all services with honcho from Procfile on development environment.
	@echo "Starting services with honcho... Press Ctrl+C to stop."
	honcho start


.PHONY: run-docker
run-docker:
	cd docker && docker-compose up
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
startdev: migratedb
	# Run all services with honcho from Procfile on development environment.
	@echo "Starting services with honcho... Press Ctrl+C to stop."
	uv run honcho start

.PHONY: migratedb
migratedb:
	@echo "Starting database migration..."
	uv run alembic upgrade head

.PHONY: docker
docker:
	docker build -f docker/Dockerfile -t vpodcasts:latest .

.PHONY: run-docker
run-docker:
	cd docker && docker-compose up

# dev container commands
.PHONY: devcontainer-up
devcontainer-up:
	devcontainer up --workspace-folder .

.PHONY: devcontainer-shell
devcontainer-shell: devcontainer-up
	devcontainer exec --workspace-folder . bash

.PHONY: devcontainer-stop
devcontainer-stop:
	docker compose -p vpodcasts_devcontainer stop

.PHONY: devcontainer-restart
devcontainer-restart: devcontainer-stop devcontainer-shell

.PHONY: devcontainer-build
devcontainer-build:
	devcontainer build --workspace-folder .

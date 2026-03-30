.PHONY: startdev
startdev: migratedb
	# Run all services with honcho from Procfile on development environment.
	@echo "Starting services with honcho... Press Ctrl+C to stop."
	uv run honcho start

.PHONY: migratedb
migratedb:
	@echo "Starting database migration..."
	uv run alembic upgrade head

.PHONY: dashboard
dashboard:
	docker run --rm \
		-e CI=true \
		-v "$$PWD:/app" \
		-w /app \
		node:24-alpine \
	  sh -c "cd /app/dashboard && corepack enable && corepack prepare pnpm@latest --activate && pnpm install && pnpm run build"


.PHONY: docker
docker:
	docker build -f docker/Dockerfile -t vpodcasts:latest .

.PHONY: all
all: dashboard docker

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

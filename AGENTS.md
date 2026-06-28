# AGENTS.md

> A guide for AI coding agents working on this repository.
> Think of this as a README for agents — providing the extra context needed to work effectively on the project.

---

## Project Overview

**VPodcasts** is a self-hosted tool that converts individual online video URLs into a private podcast RSS feed. Users paste a video URL into the web dashboard; the backend downloads the audio in the background and exposes it as a standard podcast episode.

### Architecture at a Glance

The project is a full-stack monorepo with two main components:

| Component                | Location            | Technology                                      |
| ------------------------ | ------------------- | ----------------------------------------------- |
| Backend API & RSS        | `vpodcasts/`        | Python 3.13, FastAPI, SQLModel, Taskiq, NATS    |
| Web Dashboard            | `dashboard/`        | Angular 21, Angular Material, TanStack Query    |
| Database                 | `data/vpodcasts.db` | SQLite (via SQLModel + Alembic)                 |
| Task Queue               | NATS + Taskiq       | Background audio download jobs                  |
| Package Manager (Python) | `uv`                | Used for all Python dependency management       |
| Package Manager (Node)   | `pnpm`              | Used for all Node/Angular dependency management |

---

## Repository Structure

```
vpodcasts/               # Python package — backend core
  webapp.py              # FastAPI application (API routes, RSS, SSE event stream)
  models.py              # SQLModel ORM models (Episode, DownloadTask)
  database.py            # DB session helpers and query functions
  taskiq_broker.py       # Taskiq worker — yt-dlp download tasks
  config.py              # Configuration loaded from .env
  templates/             # Jinja2 template (index.html landing page)
dashboard/               # Angular frontend (web admin dashboard)
  src/app/
    components/          # Shared/reusable Angular components
    pages/               # Route-level page components
    services/            # Angular services (API calls, etc.)
    types.ts             # Shared TypeScript types
    stores.ts            # Signal-based stores
    app.routes.ts        # Application routing
alembic/                 # Database migration scripts
  versions/              # Migration version files
data/                    # Runtime data (SQLite DB, downloaded audio files)
docker/                  # Dockerfile and related Docker build files
build/                   # Built dashboard assets (generated, do not edit)
.agents/rules/           # Agent-specific rule files (auto-loaded by context)
```

---

## Development Setup

The recommended development approach uses **Dev Containers**. Running outside a container is possible but requires NATS to be available.

### Option 1: Dev Container (Recommended)

```bash
# Install Dev Container CLI if not already installed
npm install -g @devcontainers/cli

# Start the dev container (installs all deps on first run)
make devcontainer-shell

# Inside the container — start all services
make startdev
```

Access the dashboard at [http://localhost:5180/](http://localhost:5180/).

### Option 2: Local (Manual)

Prerequisites: Python 3.13, `uv`, Node.js (see `.nvmrc`), `pnpm`, a running NATS server.

```bash
# Install Python dependencies
uv sync

# Install frontend dependencies
cd dashboard && pnpm install && cd ..

# Apply database migrations
make migratedb   # runs: uv run alembic upgrade head

# Start all services (web + taskiq worker + frontend dev server)
make startdev    # runs: uv run honcho start
```

The `Procfile` defines the three services started by `honcho`:
- `web` — FastAPI on port 5080
- `taskiq` — Taskiq worker for background downloads
- `frontend` — Angular dev server on port 4200

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the values before running:

```bash
cp .env.example .env
```

| Variable               | Default                        | Description                                                                  |
| ---------------------- | ------------------------------ | ---------------------------------------------------------------------------- |
| `BASE_URL`             | `http://localhost:8000`        | Public base URL for the RSS feed and audio links                             |
| `PODCAST_TITLE`        | `My YouTube Podcast`           | Title shown in podcast apps                                                  |
| `PODCAST_DESCRIPTION`  | *(see example)*                | Podcast description for RSS feed                                             |
| `PODCAST_LINK`         | `https://github.com/your_repo` | Link in the podcast RSS                                                      |
| `EPISODES_DIR`         | `data/episodes`                | Directory where downloaded audio files are stored                            |
| `NATS_URL`             | `nats://nats:4222`             | NATS server URL for the task queue                                           |
| `YOUTUBE_COOKIES_FILE` | *(empty)*                      | Optional path to a cookies file for yt-dlp (e.g., for age-restricted videos) |

---

## Backend (Python / FastAPI)

### Key Commands

```bash
# Run a single service in isolation
uv run fastapi dev vpodcasts/webapp.py --host 0.0.0.0 --port 5080
uv run taskiq worker vpodcasts.taskiq_broker:broker

# Database migrations
uv run alembic upgrade head          # Apply all migrations
uv run alembic revision --autogenerate -m "description"  # Create new migration

# Dependency management
uv add <package>                     # Add a new dependency to pyproject.toml
uv sync                              # Install/sync all dependencies
uv tree --outdated --depth=1         # Check for outdated packages
uvx uv-bump                          # Bump pyproject.toml deps to latest feasible versions
```

### Code Conventions

- **Python version**: 3.13 (strictly, as set in `pyproject.toml`)
- **Linting / type checking**: `basedpyright` (config in `pyproject.toml`)
- **Models**: Defined in `vpodcasts/models.py` using SQLModel. `Episode` and `DownloadTask` are the two core tables.
- **Database access**: Use the helper functions in `vpodcasts/database.py` rather than writing raw SQLModel queries directly in route handlers.
- **Background tasks**: All download/processing jobs are dispatched via Taskiq to the NATS queue. See `vpodcasts/taskiq_broker.py`.
- **Configuration**: All environment-dependent config lives in `vpodcasts/config.py` — never read `os.getenv` directly in route handlers.
- **Real-time notifications**: The backend uses NATS pub/sub + a Server-Sent Events endpoint (`GET /api/eventstream`) to push task status updates to the frontend.

### API Endpoints Summary

| Method   | Path                         | Description                                      |
| -------- | ---------------------------- | ------------------------------------------------ |
| `GET`    | `/rss`                       | RSS podcast feed (XML)                           |
| `GET`    | `/api/episodes`              | List episodes (pagination + status filter)       |
| `POST`   | `/api/add`                   | Submit a new video URL for download              |
| `POST`   | `/api/episodes/{id}/archive` | Archive an episode                               |
| `DELETE` | `/api/episodes/{id}`         | Permanently delete an episode and its audio file |
| `GET`    | `/api/tasks`                 | List recent download tasks                       |
| `GET`    | `/api/eventstream`           | SSE stream for real-time task notifications      |

### Testing

Backend tests live in `tests/`. The test suite uses **pytest** with FastAPI's `TestClient` (backed by `httpx`).

```bash
# Run all backend tests (inside the dev container):
uv run pytest
```
---

## Frontend (Angular / `dashboard/`)

> **Note:** When editing files inside `dashboard/`, additional Angular-specific guidelines apply — see `.agents/rules/angular-guidelines.md`.

### Key Commands

```bash
# From the dashboard/ directory:
pnpm install          # Install dependencies
pnpm start            # Start Angular dev server (http://localhost:4200)
pnpm run build        # Build for production
pnpm test             # Run tests with Vitest
```

### Technology Stack

- **Framework**: Angular 21 (standalone components, signals-first)
- **UI Library**: Angular Material 21
- **Data Fetching**: TanStack Query for Angular (`@tanstack/angular-query-experimental`)
- **Icons**: Lucide Angular
- **Testing**: Vitest
- **Styling**: SCSS

### Component Conventions

- All components are **standalone** (no NgModules). Do **not** set `standalone: true` in the decorator — it is the default.
- Use **signals** (`signal()`, `computed()`) for all local state.
- Always set `changeDetection: ChangeDetectionStrategy.OnPush`.
- Use Angular's native control flow (`@if`, `@for`, `@switch`) — never `*ngIf`, `*ngFor`, `*ngSwitch`.
- Use `input()` / `output()` functions instead of `@Input()` / `@Output()` decorators.
- Use `inject()` in the constructor instead of constructor parameter injection.
- Do **not** use `ngClass` or `ngStyle` — use `[class]` and `[style]` bindings instead.
- Use `providedIn: 'root'` for singleton services.

### File Structure Conventions

- **`pages/`** — Route-level components (one per page/view)
- **`components/`** — Shared/reusable presentational components
- **`services/`** — Injectable services (API calls, etc.)
- **`types.ts`** — Shared TypeScript interfaces and types
- **`stores.ts`** — Signal-based application state stores
- **`app.routes.ts`** — All route definitions (use lazy loading for page modules)

### Tests

All frontend tests live in `dashboard/src/__tests__/`. Place new tests there.

```bash
pnpm test             # Run all Vitest tests
```

---

## Building the Dashboard for Production

The production dashboard build is embedded into the Python package at `dashboard-dist/`.

```bash
# Build using Docker (used in CI/production):
make dashboard

# Build locally (from dashboard/ directory):
pnpm run build --deploy-url=/assets/ --base-href=/dashboard/
```

The built output is served by the FastAPI backend from the `dashboard-dist/browser/` directory.

---

## Docker

```bash
# Build the production Docker image
make docker          # runs: docker build -f docker/Dockerfile -t vpodcasts:latest .

# Build dashboard + Docker image together
make all
```



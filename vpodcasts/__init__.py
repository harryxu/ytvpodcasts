import os

from loguru import logger

from vpodcasts.config import PROJECT_ROOT

log_path = str(PROJECT_ROOT / "data/logs")
if not os.path.exists(log_path):
    os.makedirs(log_path)

logger.add(
    os.path.join(log_path, "app.log"),
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    encoding="utf-8",
    enqueue=True,
)

__all__ = ["logger"]

import random
import asyncio
import json

from vpodcasts.config import NATS_URL
from nats.aio.client import Client as NATS

task = {
    "id": 99999,
    "title": "Testing task",
    "status": "pending",
    "created_at": "2025-12-26T16:10:52.737290",
    "completed_at": "2025-12-26T16:11:17.173823",
    "description": None,
    "updated_at": "2025-12-26T16:07:29.662624",
    "episode_id": None,
}


async def main():
    nc = NATS()
    await nc.connect(NATS_URL)

    value = 0
    while True:
        await asyncio.sleep(random.random() * 3)
        increment = random.randint(1, 20)
        value += increment
        if value > 100:
            value = 100

        task["status"] = "processing"
        payload = {
            "type": "task",
            "progress": {
                "status": "downloading",
                "downloaded_bytes": value,
                "total_bytes": 100,
                "eta": 18,
                "speed": 296716.22079447325,
                "elapsed": 0.19812703132629395,
                "_eta_str": "00:18",
                "_speed_str": " 289.76KiB/s",
                "_percent": value / 100,
                "_percent_str": f"{value}%",
                "_total_bytes_str": "   5.30MiB",
                "_total_bytes_estimate_str": "       N/A",
                "_downloaded_bytes_str": "   3.00KiB",
                "_elapsed_str": "00:00:00",
                "_default_template": f"  {value}% of    5.30MiB at  289.76KiB/s ETA 00:18",
            },
            "task": task,
            "status": "progress",
        }

        await nc.publish("notification", json.dumps(payload).encode())

        if value == 100:
            break

    task["status"] = "success"
    await nc.publish(
        "notification",
        json.dumps({"type": "task", "task": task, "status": "success"}).encode(),
    )
    await nc.drain()


asyncio.run(main())

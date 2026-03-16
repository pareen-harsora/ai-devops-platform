import redis
import json
import time
import os

redis_host = os.getenv("REDIS_HOST", "redis")

r = redis.Redis(host=redis_host, port=6379)

print("Worker started", flush=True)

while True:
    task = r.brpop("tasks")

    if task:
        payload = json.loads(task[1])
        print("Processing:", payload, flush=True)

        time.sleep(2)

        print("Task completed")

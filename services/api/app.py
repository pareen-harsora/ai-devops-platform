from flask import Flask
import redis
import time

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Redis connection
r = redis.Redis(host="redis-service", port=6379)

# Metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total API Requests')
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency')

@app.route("/")
def home():
    REQUEST_COUNT.inc()
    start_time = time.time()

    r.rpush("tasks", "new task")

    latency = time.time() - start_time
    REQUEST_LATENCY.observe(latency)

    return "Task sent!"

#  Metrics endpoint
@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
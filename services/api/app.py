from flask import Flask, request
import redis
import json
import os

app = Flask(__name__)

redis_host = os.getenv("REDIS_HOST", "redis")

r = redis.Redis(host=redis_host, port=6379)

@app.route("/")
def home():
    return {"service": "api", "status": "running"}

@app.route("/task", methods=["POST"])
def task():
    data = request.json
    r.lpush("tasks", json.dumps(data))
    return {"message": "task queued"}

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

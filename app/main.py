from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response
import time
import random

app = FastAPI()

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of requests",
    ["endpoint"]
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Request latency"
)

@app.get("/price")
def get_price():
    start = time.time()

    # simula lógica de negócio
    time.sleep(random.uniform(0.05, 0.2))
    price = random.randint(90, 110)

    REQUEST_COUNT.labels(endpoint="/price").inc()
    REQUEST_LATENCY.observe(time.time() - start)

    return {
        "price": price,
        "currency": "USD",
        "version": "v1"
    }

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

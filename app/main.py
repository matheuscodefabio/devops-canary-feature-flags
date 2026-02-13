from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response
from UnleashClient import UnleashClient
import time
import os

app = FastAPI()

# =============================================================================
# PROMETHEUS METRICS
# =============================================================================

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Request latency",
    ["endpoint"]
)

FEATURE_FLAG_USAGE = Counter(
    "app_feature_flag_usage_total",
    "Feature flag usage",
    ["flag_name", "flag_status"]
)

PRICE_CALCULATION = Counter(
    "app_price_calculation_total",
    "Price calculation method used",
    ["method"]
)

# =============================================================================
# UNLEASH CLIENT
# =============================================================================

UNLEASH_URL = os.getenv(
    "UNLEASH_URL",
    "http://unleash.unleash.svc.cluster.local:4242/api"
)

UNLEASH_TOKEN = os.getenv(
    "UNLEASH_TOKEN",
    "*:*.unleash-insecure-api-token"
)

APP_NAME = os.getenv("APP_NAME", "price-api")

unleash_client = UnleashClient(
    url=UNLEASH_URL,
    app_name=APP_NAME,
    custom_headers={"Authorization": UNLEASH_TOKEN},
)

@app.on_event("startup")
def startup_event():
    unleash_client.initialize_client()

# =============================================================================
# BUSINESS LOGIC
# =============================================================================

def calculate_price_v1(base_price: float):
    return base_price

def calculate_price_v2(base_price: float):
    discount = 0.10
    return round(base_price * (1 - discount), 2)

# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/price")
def get_price(amount: float = 100.0):
    start_time = time.time()

    try:
        use_new_pricing = unleash_client.is_enabled("new-pricing-algorithm")

        FEATURE_FLAG_USAGE.labels(
            flag_name="new-pricing-algorithm",
            flag_status="enabled" if use_new_pricing else "disabled",
        ).inc()

        if use_new_pricing:
            final_price = calculate_price_v2(amount)
            method = "v2_discounted"
        else:
            final_price = calculate_price_v1(amount)
            method = "v1_standard"

        PRICE_CALCULATION.labels(method=method).inc()

        REQUEST_COUNT.labels(
            method="GET",
            endpoint="/price",
            status="200"
        ).inc()

        REQUEST_LATENCY.labels(endpoint="/price").observe(
            time.time() - start_time
        )

        return {
            "base_price": amount,
            "final_price": final_price,
            "pricing_method": method,
            "feature_flag_active": use_new_pricing,
        }

    except Exception as e:
        REQUEST_COUNT.labels(
            method="GET",
            endpoint="/price",
            status="500"
        ).inc()

        return {"error": str(e)}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

@app.get("/api/info")
def info():
    return {
        "app": APP_NAME,
        "version": os.getenv("APP_VERSION", "v1"),
        "unleash_url": UNLEASH_URL,
        "endpoints": ["/health", "/metrics", "/price", "/api/info"],
    }

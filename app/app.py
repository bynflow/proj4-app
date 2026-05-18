from flask import Flask, Response, request, render_template
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import os

app = Flask(__name__)

# Prometheus counter for application requests
REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total app requests",
    ["method", "endpoint"],
)

REQUEST_LATENCY = Histogram(
    "app_request_duration_seconds",
    "Request latency in seconds",
    ["method", "endpoint"],
)

REQUEST_ERRORS = Counter(
    "app_errors_total",
    "Total app errors",
    ["method", "endpoint", "status"],
)


@app.route("/", methods=["GET", "POST"])
def index():
    start_time = time.time()
    REQUEST_COUNT.labels(method=request.method, endpoint="/").inc()

    try:
        if request.method == "POST":
            expr = request.form.get("number", "").strip()

            if not expr.isdigit():
                REQUEST_ERRORS.labels(
                    method=request.method,
                    endpoint="/",
                    status="400",
                ).inc()
                return render_template(
                    "number_square.html",
                    error="Please enter a valid non-negative integer.",
                ), 400

            result = int(expr) ** 2

            return render_template(
                "result.html",
                number=expr,
                square=result,
                container_name=os.environ.get("CONTAINER_NAME", "unknown"),
                public_ip=os.environ.get("PUBLIC_IP", "unknown"),
            )

        return render_template("number_square.html")
    finally:
        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint="/",
        ).observe(time.time() - start_time)


@app.get("/health")
def health():
    REQUEST_COUNT.labels(method="GET", endpoint="/health").inc()
    return {"status": "ok"}, 200


@app.get("/metrics")
def metrics():
    REQUEST_COUNT.labels(method="GET", endpoint="/metrics").inc()
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


# gitops-observability-platform-app

Secure observable Flask application for a multi-repository GitOps Kubernetes platform.

This repository contains the **application layer** of Project 4: application code, tests, CI, container build logic, image publishing, security scanning, and Prometheus instrumentation.

The Kubernetes environment and deployment governance are intentionally separated into a dedicated environment repository:

* [`gitops-observability-platform-env`](https://github.com/bynflow/gitops-observability-platform-env)

This separation reflects a production-style GitOps model where application delivery and environment governance have different responsibilities.

---

## Project role

`gitops-observability-platform-app` is responsible for:

* Flask application source code
* automated tests
* Docker image build
* immutable image publishing to GHCR
* GitHub Actions CI
* Trivy container image scanning
* Python dependency scanning with `pip-audit`
* Prometheus application metrics

It does **not** own:

* Kubernetes manifests
* environment overlays
* ArgoCD Applications
* RBAC / NetworkPolicy / Ingress / TLS configuration
* cluster-side deployment governance

Those responsibilities belong to `gitops-observability-platform-env`.

---

## Architecture context

```text
Developer
   |
   | push code
   v
GitHub repository: gitops-observability-platform-app
   |
   | GitHub Actions
   | - tests
   | - Docker build
   | - Trivy image scan
   | - GHCR push
   v
GHCR image: ghcr.io/bynflow/gitops-observability-platform-app:sha-*
   |
   | selected by env repo
   v
gitops-observability-platform-env
   |
   | ArgoCD reconciliation
   v
Kubernetes runtime
```

The application repository produces immutable artifacts.
The environment repository decides which artifact runs in each environment.

---

## Application endpoints

| Endpoint   | Purpose                     |
| ---------- | --------------------------- |
| `/`        | Main Flask application page |
| `/health`  | Health check endpoint       |
| `/metrics` | Prometheus metrics endpoint |

---

## Observability

The application exposes Prometheus-compatible metrics through:

```text
/metrics
```

Implemented metrics include:

* request counters
* error counters
* request latency histograms

This provides a first application-level observability baseline based on golden signals:

* traffic
* errors
* latency

Example metrics:

```text
app_requests_total
app_errors_total
app_request_duration_seconds
```

---

## Security and DevSecOps baseline

This repository includes a minimal but real DevSecOps baseline:

* Trivy image vulnerability scanning
* GitHub Actions security gate for critical vulnerabilities
* Python dependency audit using `pip-audit`
* generated dependency lock file excluded from Git
* immutable image tags based on commit SHA

The security model distinguishes between:

```text
Image scan       → container artifact vulnerabilities
Dependency scan  → Python library vulnerabilities
Secret handling  → managed at Kubernetes runtime in gitops-observability-platform-env
```

---

## CI pipeline

The GitHub Actions pipeline performs:

1. Python test execution
2. Docker image build
3. immutable image tagging
4. GHCR image publishing
5. Trivy container image scan

Images are published using SHA-based tags:

```text
ghcr.io/bynflow/gitops-observability-platform-app:sha-<commit>
```

This enables deterministic promotion through the GitOps environment repository.

---

## Local development

Run tests:

```bash
python -m pytest -q
```

Run the application locally:

```bash
python -m app.app
```

Check health:

```bash
curl http://localhost:5000/health
```

Check metrics:

```bash
curl http://localhost:5000/metrics
```

---

## Repository structure

```text
gitops-observability-platform-app/
├── app/
│   ├── app.py
│   └── templates/
├── tests/
├── Dockerfile
├── requirements.txt
├── pytest.ini
└── .github/workflows/
```

---

## What this repository demonstrates

This repository demonstrates:

* application-level CI
* containerized Python application delivery
* immutable artifact production
* Prometheus application instrumentation
* security scanning in CI
* separation between application ownership and environment ownership
* portfolio-grade DevOps workflow design

---

## Related repository

Environment and GitOps governance repository:

* [`gitops-observability-platform-env`](https://github.com/bynflow/gitops-observability-platform-env)

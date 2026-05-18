# proj4-app

Application repository for Project 4.

This repository contains:

* Flask application
* tests
* Docker build logic
* CI pipeline
* security scanning
* Prometheus metrics instrumentation

The deployment and environment governance are intentionally separated into a dedicated environment repository:

* proj4-env

This separation reflects a production-style GitOps architecture.

---

## Features

* Flask application
* `/health` endpoint
* `/metrics` endpoint (Prometheus)
* pytest test suite
* Docker containerization
* GitHub Actions CI
* GHCR image publishing
* Trivy image scanning
* pip-audit dependency scanning

---

## Observability

The application exports Prometheus metrics through:

```text
/metrics
```

Metrics include:

* request counters
* latency histograms
* error counters

---

## Security

Implemented security baseline:

* container image scanning
* dependency vulnerability scanning
* Kubernetes RBAC
* NetworkPolicy
* Kubernetes Secrets baseline

---

## Repository role

This repository owns:

* application code
* tests
* build pipeline
* container image

This repository does NOT own:

* Kubernetes environment manifests
* deployment governance
* cluster configuration

Those responsibilities belong to:

* proj4-env

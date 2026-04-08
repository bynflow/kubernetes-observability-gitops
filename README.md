# Kubernetes Observability & GitOps — Project 3

## Overview

A production-grade DevOps system implementing:

* CI (GitHub Actions)
* Containerization (Docker + GHCR)
* GitOps (ArgoCD)
* Kubernetes (k3s)
* Observability (Prometheus + Grafana)
* Test-driven development (pytest)

The system is designed to be **deterministic, reproducible, and environment-aware**, with strict separation between build, delivery, and deployment.

---

## Architecture

### Architecture overview

````mermaid
graph TD

A[Developer] --> B[Git Push]
B --> C[GitHub Repository]
C --> D[GitHub Actions CI]
D --> E[Build & Test (pytest)]
E --> F[GHCR (sha-* image)]
F --> G[Update Git (dev overlay)]
G --> H[ArgoCD]
H --> I1[K8s: dev (auto-sync)]
H --> I2[K8s: staging (manual)]
H --> I3[K8s: prod (manual)]
```mermaid
graph LR
A[Developer] --> B[GitHub Repo]
B --> C[GitHub Actions CI]
C --> D[GHCR Image Registry]
D --> E[GitOps Update (dev overlay)]
E --> F[ArgoCD]
F --> G1[dev namespace]
F --> G2[staging namespace]
F --> G3[prod namespace]
````

CI builds immutable images which are propagated via Git into environment overlays and deployed by ArgoCD.

---

## Key Design Decisions

### DEC-001 — CI/CD Separation

* CI is repository-centric (GitHub Actions)
* CD is cluster-centric (ArgoCD)

This ensures:

* clean responsibility boundaries
* reproducibility

---

### DEC-002 — Immutable Image Tags

Images are tagged as:

```
sha-<commit>
```

No mutable tags (like `latest`) are used.

Benefits:

* deterministic deployments
* safe rollback
* traceability

---

### DEC-003 — Git as Source of Truth

Git stores:

* structure
* environment configuration

Git does NOT store:

* runtime state
* mutable versions

---

### DEC-004 — Promotion & Rollback Strategy

Promotion:

* performed via Git (overlay update)
* environment-specific

Rollback:

* redeploy previous SHA

```
newTag: sha-previous
```

---

## Project Structure

```
.
├── app/
├── tests/
├── k8s/
│   ├── base/
│   └── overlays/
│       ├── dev/
│       ├── staging/
│       └── prod/
├── .github/workflows/
├── Dockerfile
├── requirements.txt
├── pytest.ini
```

---

## Application

Minimal Flask application:

* `/` → input form
* POST → square computation
* `/health`
* `/metrics`

Example:

```
Input: 5
Output: 25
```

---

## Testing Strategy (TDD-style)

Tests validate:

* endpoints
* input validation
* edge cases
* health endpoint

Run locally:

```
python -m pytest -q
```

Configuration:

```
[pytest]
testpaths = tests
```

Principles:

* tests precede deployment
* CI enforces correctness
* no build without passing tests

---

## CI Pipeline

Stages:

1. Test (pytest)
2. Build (Docker)
3. Push (GHCR)
4. Update dev overlay (GitOps trigger)

Key guarantee:

```
No artifact is produced unless tests pass
```

---

## Deployment Model

Namespaces:

```
proj3-dev
proj3-staging
proj3-prod
```

Each environment is isolated and independently controlled.

---

## GitOps (ArgoCD)

| Environment | Sync Mode | Purpose             |
| ----------- | --------- | ------------------- |
| dev         | auto-sync | continuous delivery |
| staging     | manual    | validation          |
| prod        | manual    | controlled release  |

Behavior:

* dev deploys automatically after CI
* staging/prod require explicit promotion

---

## Promotion Flow

```
dev → staging → prod
```

Promotion = updating `kustomization.yaml` in target environment.

---

## Rollback Strategy

Rollback is deterministic:

* select previous SHA
* update overlay
* redeploy via ArgoCD

---

## Observability

Prometheus:

* scrapes `/metrics`
* tracks request counters

Grafana:

* visual dashboards
* validates runtime behavior

---

## Security

* GHCR private images
* Kubernetes `imagePullSecrets`
* controlled image access

---

## What This Project Demonstrates

* full DevOps lifecycle
* GitOps deployment model
* immutable infrastructure approach
* environment-based promotion
* integrated testing strategy
* observability-first mindset

---

## Key Takeaway

```
This project demonstrates how a system is designed, controlled, and evolved
```

with deterministic, reproducible, and auditable behavior.

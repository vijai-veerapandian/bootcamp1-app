# bootcamp1-app

The **application** half of the bootcamp project: a deliberately tiny, stateless
web app whose only job is to give the infra (EKS / Terraform / CI-CD) something
real to build, ship, and run. A static page calls a JSON API that reports which
pod served the request — handy for watching scaling and load balancing.

The deployment side (Terraform, k8s manifests, Helm chart, ArgoCD) lives in the
separate **`bootcamp1-infra`** repo.

```
┌──────────┐    HTTP     ┌──────────────┐   /api/*    ┌────────────┐
│ Browser  │────────────▶│  frontend     │────────────▶│  backend    │
│          │             │  (nginx)      │             │  (FastAPI)  │
└──────────┘             └──────────────┘             └────────────┘
        static page                         stateless — no database
```

## Layout

```
backend/      FastAPI service (Python 3.12), stateless — no DB
frontend/    Static page (HTML/JS/CSS) served by nginx
.github/      CI: test, build, and push images to ECR on push to main
docker-compose.yml   One-command local dev stack
```

## Local development

Requires Docker + Docker Compose.

```bash
docker compose up --build
# frontend → http://localhost:8080   (click "Call backend")
# backend  → http://localhost:8000/docs
```

Quick checks:

```bash
curl -s localhost:8000/api/info     # {"message":"...","hostname":"<container>"}
curl -s localhost:8080/api/info     # same, through nginx's /api proxy

# watch load-balancing across replicas
docker compose up --build --scale backend=3
# repeat the curl — the hostname rotates across the 3 backend containers
```

Backend unit tests:

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
```

## API

| Method | Path         | Purpose                                          |
| ------ | ------------ | ------------------------------------------------ |
| GET    | `/api/info`  | Returns a greeting + the serving pod's hostname  |
| GET    | `/healthz`   | Liveness probe                                   |
| GET    | `/readyz`    | Readiness probe                                  |

## CI/CD (GitOps)

`.github/workflows/ci.yml`:

1. **backend-test** — `pytest`.
2. **frontend-build** — sanity-builds the frontend image.
3. **publish** (main only) — builds both images and pushes them to ECR, tagged
   with the commit SHA and `latest`. Requires the `AWS_ROLE_TO_ASSUME` secret
   (OIDC role) and matching ECR repos provisioned by `bootcamp1-infra`.
4. **update-gitops** (opt-in) — bumps the image tag in the `bootcamp1-infra`
   Helm values so ArgoCD deploys the new build. This repo never deploys
   directly; it only builds the image and hands the tag to the GitOps repo.
   Enable by setting the `GITOPS_ENABLED` variable + `GITOPS_TOKEN` secret (see
   the comments in the workflow).

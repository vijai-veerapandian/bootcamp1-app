"""Minimal stateless FastAPI service.

No database, no persistence — every pod just answers requests out of memory.
`/api/info` reports the pod's hostname, which makes it easy to watch the EKS
Deployment scale and the load balancer spread traffic across replicas. The app
is intentionally trivial: the interesting part of this project is the
Terraform / EKS / CI-CD around it, not the service itself.
"""

from __future__ import annotations

import os
import socket

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
GREETING = os.getenv("GREETING", "Hello from the backend 👋")

app = FastAPI(title="bootcamp1-app", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in CORS_ORIGINS.split(",") if o.strip()],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    """Liveness probe — cheap and dependency-free."""
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict[str, str]:
    """Readiness probe. Stateless, so a pod is ready as soon as it's up."""
    return {"status": "ready"}


@app.get("/api/info")
def info() -> dict[str, str]:
    """Return which pod served the request — handy for watching scaling/LB."""
    return {"message": GREETING, "hostname": socket.gethostname()}

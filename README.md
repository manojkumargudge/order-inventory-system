# Order & Inventory Management System

A backend system for managing products, stock and customer orders. It is built with **FastAPI** and **PostgreSQL**, uses **JWT authentication**, and is deployed to **AWS ECS** through a **Jenkins CI/CD pipeline**.

![Python](https://img.shields.io/badge/python-3.14-blue)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688)
![PostgreSQL](https://img.shields.io/badge/DB-PostgreSQL-336791)
![Redis](https://img.shields.io/badge/cache-Redis-DC382D)
![Celery](https://img.shields.io/badge/jobs-Celery-37814A)
![Docker](https://img.shields.io/badge/container-Docker-2496ED)
![AWS](https://img.shields.io/badge/cloud-AWS%20ECS-FF9900)

---

## Features

- Async REST API with automatic Swagger docs
- JWT authentication with hashed passwords
- Async PostgreSQL access with SQLAlchemy 2 and asyncpg
- Database migrations with Alembic
- Background jobs with Celery and Redis
- Linting (ruff), type checking (mypy) and tests (pytest) in CI
- Containerized with Docker, deployed to AWS ECS from Jenkins

---

## System architecture

```mermaid
flowchart LR
    C([Client]) -->|HTTPS + JWT| API[FastAPI service<br/>AWS ECS]

    subgraph App[Application]
        API --> AUTH[Auth<br/>JWT + password hashing]
        API --> BL[Business logic<br/>Orders and Inventory]
        BL --> REPO[Data access<br/>SQLAlchemy async]
        BL -.->|enqueue| Q[(Redis<br/>broker)]
    end

    REPO --> DB[(PostgreSQL)]
    Q --> W[Celery worker]
    W --> DB

    classDef store fill:#e8f1ff,stroke:#3b82f6,color:#111
    classDef svc fill:#e9f9ee,stroke:#22c55e,color:#111
    class DB,Q store
    class API,W svc
```

---

## Order flow

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant A as FastAPI
    participant S as Business logic
    participant D as PostgreSQL

    C->>A: Login with credentials
    A->>D: Verify user
    A-->>C: JWT access token
    C->>A: Place order (Bearer token)
    A->>A: Validate token and input
    A->>S: Create order
    S->>D: BEGIN transaction
    S->>D: Check and reduce stock
    alt Enough stock
        S->>D: Save order
        S->>D: COMMIT
        A-->>C: Order confirmed
    else Not enough stock
        S->>D: ROLLBACK
        A-->>C: Error, stock not available
    end
```

---

## CI/CD pipeline

Every push to `main` runs this Jenkins pipeline (`Jenkinsfile`):

```mermaid
flowchart LR
    A[Checkout] --> B[Lint<br/>ruff]
    B --> C[Type check<br/>mypy]
    C --> D[Test<br/>pytest + Postgres 16]
    D --> E[Build<br/>Docker image]
    E --> F[Push to<br/>AWS ECR]
    F --> G[Register new<br/>ECS task definition]
    G --> H[Update<br/>ECS service]
    H --> I{Service<br/>stable?}
    I -->|Yes| J([Deployed])
    I -->|No| K([Build fails])

    classDef ok fill:#e9f9ee,stroke:#22c55e,color:#111
    classDef check fill:#fff4e5,stroke:#f59e0b,color:#111
    class B,C,D check
    class J ok
```

- **Image tag:** the Git commit hash, so every deployment can be traced to code.
- **Tests:** run against a real PostgreSQL 16 container, not a mock.
- **Region:** `ap-south-1` (Mumbai).
- **Rollout:** a new ECS task definition is registered, then the service is updated and Jenkins waits until it is stable.

---

## Tech stack

| Layer | Tool |
|---|---|
| API | FastAPI, Uvicorn, Pydantic v2, pydantic-settings |
| Database | PostgreSQL, SQLAlchemy 2 (async), asyncpg |
| Migrations | Alembic |
| Auth | JWT (python-jose), Argon2 / bcrypt password hashing |
| Background jobs | Celery, Redis |
|
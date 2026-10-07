# Order Inventory System

![Python](https://img.shields.io/badge/Python-3.14%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-4169E1?logo=postgresql&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-Jenkins-D24939?logo=jenkins&logoColor=white)

**Order Inventory System** is an asynchronous, API-first backend for managing the complete order and inventory lifecycle. It provides authenticated workflows for users, products, customers, orders, payments, and stock movements, with an administrator surface for operational visibility and control.

Built with FastAPI and SQLAlchemy 2, the service is designed around clear API, service, repository, and persistence boundaries. It includes Alembic migrations, interactive OpenAPI documentation, automated quality checks, and Docker/Jenkins assets for AWS ECS delivery.

> **Project status:** The repository includes the application, migration history, tests, container image, and deployment assets. Review environment-specific infrastructure, observability, scaling, and secret-management settings before using it in production.

## Why this project

The system centralizes the operational data needed by an order-driven business:

- Maintain a searchable product catalog and monitor stock levels.
- Create and manage customer orders through controlled status transitions.
- Record payments and payment-state changes.
- Track stock changes as auditable inventory transactions.
- Give administrators dashboards, order visibility, restocking, low-stock reporting, and role management.
- Expose a typed, self-documenting API that is straightforward to integrate with web, mobile, or internal clients.

## Capabilities

### Authentication and users

- User registration and login
- OAuth2 password flow with bearer JWTs
- Password hashing and token validation
- Current-user profile endpoint
- Role-aware access control for administrator operations

### Products and inventory

- Product create, read, update, and delete operations
- Search by product name or description
- Price-range filtering
- In-stock filtering
- Configurable sorting and pagination
- Low-stock and out-of-stock views
- Restocking and stock adjustments
- Inventory transaction history for purchases, sales, returns, adjustments, and damaged stock

### Orders, customers, and payments

- Customer profile create, read, update, and delete operations
- Order creation and retrieval
- Order cancellation and status updates
- Payment creation, retrieval, and status transitions
- Administrative order and dashboard views

## Architecture

```text
Client
  │
  ▼
FastAPI routes (/api/v1)
  │  request validation, authentication, response models
  ▼
Service layer
  │  business rules and workflow orchestration
  ▼
Repository layer
  │  persistence queries
  ▼
SQLAlchemy 2 async ORM
  │
  ▼
PostgreSQL
```

Supporting concerns are isolated in:

- `src/core/` — settings, security, dependencies, and enums
- `src/db/` — asynchronous engine and session management
- `alembic/` — synchronous migration environment and revision history
- `ecs/` — ECS task-definition rendering and deployment inputs

## Technology stack

| Area | Technology |
| --- | --- |
| Runtime | Python 3.14+ |
| API framework | FastAPI, Uvicorn |
| Validation and settings | Pydantic 2, Pydantic Settings |
| Database | PostgreSQL 14+, SQLAlchemy 2 async ORM, `asyncpg` |
| Migrations | Alembic |
| Authentication | JWT via `python-jose`, Passlib password hashing |
| Development quality | Pytest, pytest-asyncio, Ruff, mypy |
| Packaging | Docker multi-stage image |
| Delivery | Jenkins, Amazon ECR, Amazon ECS |

## Quick start

### Prerequisites

- Python 3.14 or newer
- PostgreSQL 14 or newer
- Git
- Docker, if you want to run the container or database locally

### 1. Clone the repository

```bash
git clone https://github.com/manojkumargudge/order-inventory-system.git
cd order-inventory-system
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

Install the resolved dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

For editable development installation with the optional development dependencies:

```bash
python -m pip install -e ".[dev]"
```

### 4. Configure the application

Copy [`.env.example`](.env.example) to `.env`:

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Set a unique `SECRET_KEY`, valid PostgreSQL credentials, and a valid `DATABASE_URL`. Never commit `.env`.

### 5. Apply migrations and start the API

```bash
alembic upgrade head
uvicorn src.main:app --reload
```

The service starts at <http://localhost:8000>.

## API guide

### Documentation and health

| Resource | URL |
| --- | --- |
| Swagger UI | <http://localhost:8000/docs> |
| ReDoc | <http://localhost:8000/redoc> |
| OpenAPI schema | <http://localhost:8000/openapi.json> |
| Liveness endpoint | <http://localhost:8000/health> |

### Resource map

All business endpoints are versioned under `/api/v1`.

| Domain | Prefix | Typical operations |
| --- | --- | --- |
| Authentication | `/api/v1/auth` | Register, login, inspect current user |
| Products | `/api/v1/products` | Catalog CRUD, search, stock views, restocking |
| Orders | `/api/v1/orders` | Create, list, retrieve, cancel, update status |
| Customers | `/api/v1/customers` | Manage the current customer profile |
| Payments | `/api/v1/payments` | Create, list, retrieve, update payment state |
| Inventory | `/api/v1/inventory` | Record inventory transactions |
| Administration | `/api/v1/admin` | Dashboard, all orders, restocking, roles |

### Authentication flow

1. Register a user with `POST /api/v1/auth/register`.
2. Log in with `POST /api/v1/auth/login`.
3. Use the returned `access_token` on protected requests.

The login endpoint accepts OAuth2 form fields:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=your-username&password=your-password"
```

Use the token as a bearer token:

```bash
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <access-token>"
```

### Product listing example

The product collection supports search, price filtering, stock filtering, sorting, and pagination:

```bash
curl "http://localhost:8000/api/v1/products?search=keyboard&in_stock=true&page=1&page_size=20" \
  -H "Authorization: Bearer <access-token>"
```

For the complete request and response schemas, use Swagger UI or the generated OpenAPI document rather than relying on examples in this README.

## Configuration reference

Settings are loaded from `.env` through Pydantic Settings. See [`.env.example`](.env.example) for the starter template.

| Variable | Required | Purpose |
| --- | --- | --- |
| `APP_NAME` | Yes | Service display name |
| `APP_VERSION` | Yes | Application/API version |
| `ENVIRONMENT` | No | Environment name; defaults to development |
| `DEBUG` | No | Debug mode; use `False` outside local development |
| `SECRET_KEY` | Yes | Secret used to sign JWTs |
| `ALGORITHM` | No | JWT signing algorithm; defaults to `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | JWT lifetime; defaults to `30` |
| `POSTGRES_HOST` | Yes | PostgreSQL hostname |
| `POSTGRES_PORT` | Yes | PostgreSQL port |
| `POSTGRES_DB` | Yes | PostgreSQL database name |
| `POSTGRES_USER` | Yes | PostgreSQL username |
| `POSTGRES_PASSWORD` | Yes | PostgreSQL password |
| `DATABASE_URL` | Yes | Async database connection URL |
| `BACKEND_CORS_ORIGINS` | No | Comma-separated allowed origins |
| `LOG_LEVEL` | No | Application log level; defaults to `INFO` |

## Database migrations

Check the current revision:

```bash
alembic current
```

Create and apply a migration after changing SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe the schema change"
alembic upgrade head
```

Always review autogenerated migrations before applying them. For production deployments, run migrations as an explicit release step and verify rollback or recovery procedures for schema changes.

## Testing and quality gates

Run the test suite:

```bash
pytest
```

Run linting and type checking:

```bash
ruff check src/
mypy src/
```

The Jenkins test stage starts PostgreSQL 16 in Docker and runs the suite against an isolated test database. Local database-backed tests require a reachable PostgreSQL instance and a test `DATABASE_URL`.

## Docker

Build the production image:

```bash
docker build -t order-inventory-system:local .
```

Run it with environment values supplied from a secure file:

```bash
docker run --rm \
  --env-file .env \
  --publish 8000:8000 \
  order-inventory-system:local
```

The image:

- Uses a multi-stage Python 3.14 build.
- Keeps build tools out of the runtime stage.
- Runs as the non-root `appuser`.
- Exposes port `8000`.
- Runs `alembic upgrade head` before starting Uvicorn.
- Defines a Docker health check against `/health`.

## CI/CD and AWS deployment

[`Jenkinsfile`](Jenkinsfile) defines the delivery flow for the `main` branch:

1. Checkout
2. Ruff linting
3. mypy type checking
4. Pytest with PostgreSQL 16 in Docker
5. Docker image build
6. Push to Amazon ECR
7. Render and register an ECS task definition
8. Update the ECS service

The pipeline currently targets `ap-south-1` and expects:

- Jenkins credentials with ID `aws-credentials`
- An existing ECR repository named `order-inventory-system`
- An ECS cluster and service
- An ECS task definition family matching the pipeline configuration
- IAM permissions for ECR, ECS, and the configured secret store

Before using the deployment assets in another account or environment, review [`ecs/task-definition.json`](ecs/task-definition.json), [`ecs/render_task_def.py`](ecs/render_task_def.py), and the values in [`Jenkinsfile`](Jenkinsfile). Provide `DATABASE_URL` and `SECRET_KEY` through AWS Secrets Manager or another managed secret system, not through source control or a baked image layer.

## Project structure

```text
.
├── src/
│   ├── api/v1/           # Versioned HTTP routes by domain
│   ├── core/             # Settings, security, dependencies, and enums
│   ├── db/               # Async engine and session management
│   ├── models/           # SQLAlchemy persistence models
│   ├── repositories/     # Database query and persistence logic
│   ├── schemas/          # Pydantic request and response models
│   └── services/         # Business rules and orchestration
├── alembic/              # Migration environment and revisions
├── ecs/                  # ECS task-definition helper files
├── Dockerfile            # Multi-stage production image
├── Jenkinsfile           # CI/CD pipeline
├── pyproject.toml        # Project metadata and optional dependencies
├── requirements.txt      # Resolved runtime and tooling dependencies
└── test_security.py      # Security-focused tests
```

## Security and production checklist

- [ ] Generate a long, random, environment-specific `SECRET_KEY`.
- [ ] Set `DEBUG=False` outside local development.
- [ ] Keep `.env`, credentials, tokens, and database dumps out of Git.
- [ ] Store production secrets in AWS Secrets Manager or an equivalent managed store.
- [ ] Restrict `BACKEND_CORS_ORIGINS` to trusted application origins.
- [ ] Run the API behind TLS and an appropriate network boundary.
- [ ] Apply migrations through a controlled release process.
- [ ] Configure database backups, retention, and restore testing.
- [ ] Add centralized logs, metrics, alerting, and request tracing.
- [ ] Review ECS CPU, memory, health-check, autoscaling, and IAM settings for the target workload.
- [ ] Pin and regularly review dependency versions and security advisories.

## Contributing

1. Create a focused branch.
2. Make the smallest coherent change.
3. Add or update tests for behavioral changes.
4. Run:

   ```bash
   pytest
   ruff check src/
   mypy src/
   ```

5. Review generated migrations and deployment changes carefully.
6. Open a pull request with a concise summary, test results, and any configuration or migration notes.

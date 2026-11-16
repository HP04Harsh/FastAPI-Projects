# FastAPI Projects

A collection of small FastAPI examples covering routing, query and path
parameters, Pydantic response models, and custom exception handlers.

## Projects

### FastAPI Foundation

`01_fastapi_foundation.py` implements a sample order-service API:

- `GET /` and `GET /about` provide health and service metadata.
- `GET /orders`, `GET /orders/status`, and `GET /orders/active` return sample order data.
- `GET /debug/request-info` demonstrates access to request details.

### ChaiPoint Menu API

`ChaiPoint/` implements a read-only menu API with category and availability
filters, plus lookup by item ID.

- `GET /menu?category=chai&available_only=true`
- `GET /menu/{item_id}`

### Indian PIN Code Lookup API

`pincode-api/` demonstrates single and bulk lookup against a small in-memory
sample dataset, request validation, and custom error responses.

- `GET /pincode/{code}`
- `POST /pincode/lookup` with `{"pincode": "560001"}`
- `POST /pincode/bulk` with `{"pincodes": ["560001", "110001"]}`

## Setup

From the project root, create and activate a virtual environment, then install
the shared dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install fastapi "uvicorn[standard]"
```

Run the foundation API from the project root:

```powershell
uvicorn 01_fastapi_foundation:app --reload
```

Run either subproject from its own directory:

```powershell
Set-Location .\ChaiPoint
uvicorn main:app --reload
```

```powershell
Set-Location ..\pincode-api
uvicorn main:app --reload
```

Each server uses `http://127.0.0.1:8000` by default. Interactive API
documentation is available at `/docs`.

These APIs use in-memory sample data and are intended for learning and local
development, not production use. On managed Windows devices, Application
Control may block Uvicorn; use an administrator-approved development
environment.

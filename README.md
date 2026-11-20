# FastAPI Projects

A collection of independent FastAPI learning projects. Each directory is a
standalone application with its own dependencies, data, and startup command;
there is no shared root-level application or requirements file.

Most projects use in-memory sample data or a local SQLite database. The RAG
and Wakeel projects also depend on external services. These examples are for
learning and local development, not production deployment.

## Project map

| Path | What it demonstrates | Run command |
| --- | --- | --- |
| `01_fastapi_foundation.py` | Basic routes, request inspection, and static order responses | From the repository root: `uvicorn 01_fastapi_foundation:app --reload` |
| `fastapi-contextmanager.py` | FastAPI lifespan startup/shutdown pattern | Standalone lifespan example |
| `ChaiPoint/` | Menu API with category and availability filters | From `ChaiPoint/`: `uvicorn main:app --reload` |
| `ChaiPoint-1/` | Earlier menu API with category filtering | From `ChaiPoint-1/`: `uvicorn main:app --reload` |
| `auto-fill-city-api/` | PIN-code lookup with custom validation and error handlers | From `auto-fill-city-api/`: `uvicorn main:app --reload` |
| `pincode-api/` | PIN-code lookup by path or request body, including bulk lookup | From `pincode-api/`: `uvicorn main:app --reload` |
| `PizzaDelivery/` | Pizza stock records backed by SQLite and SQLModel | From `PizzaDelivery/`: `uvicorn main:app --reload` |
| `Rangmanch-1/` | Theatre reviews with filtering, pagination, ratings, and CRUD | From `Rangmanch-1/`: `uvicorn main:app --reload` |
| `Rangmanch/` | Earlier reviews API attempt | Incomplete: `reviews.py` does not currently define the router imported by `main.py`. Use `Rangmanch-1/` for the working version. |
| `tiffin_delivery/` | Tiffin order tracking, status updates, and daily statistics | From `tiffin_delivery/`: `uvicorn main:app --reload` |
| `kitab_exchange/` | Book listings and users with API-key-protected writes | From `kitab_exchange/`: `uvicorn main:app --reload` |
| `RAG-API/` | PDF indexing and retrieval using Hugging Face embeddings, Qdrant, and Groq | From `RAG-API/`: `uvicorn app.main:app --reload` |
| `wakeel_contract_api_groq/` | Contract upload, text extraction, and Groq-based analysis with MongoDB | From `wakeel_contract_api_groq/`: `uvicorn app.main:app --reload` |

Interactive API documentation is available at `http://127.0.0.1:8000/docs`
for each running API.

## Run a project

Use a separate virtual environment for each project. In PowerShell, for
example:

```powershell
Set-Location .\ChaiPoint
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirement.txt
uvicorn main:app --reload
```

Dependency manifests are named `requirement.txt` or `requirements.txt`
depending on the project. Install only the manifest for the application you
want to run.

For the root-level foundation example:

```powershell
python -m pip install fastapi "uvicorn[standard]"
uvicorn 01_fastapi_foundation:app --reload
```

## External services and configuration

### RAG API

1. Copy `RAG-API/.env.example` to `RAG-API/.env` and set `GROQ_API_KEY`.
2. Start Qdrant from the project directory with `docker compose up -d`.
3. Install `RAG-API/requirement.txt`.
4. Put a PDF at `RAG-API/data/Sample.pdf`, then run `python -m app.index`.
5. Start the API with `uvicorn app.main:app --reload`.

The indexer and query route use the `RAG-AI` collection and the
`sentence-transformers/all-MiniLM-L6-v2` model (384 dimensions). If the
configured Qdrant collection has an incompatible vector configuration, the
indexer deletes and recreates that collection; its existing vectors will be
lost.

### Wakeel contract API

1. Copy `wakeel_contract_api_groq/.env.example` to
   `wakeel_contract_api_groq/.env`. Replace the MongoDB password and provide
   a valid `GROQ_API_KEY`.
2. Start MongoDB from the project directory with `docker compose up -d`.
3. Install `wakeel_contract_api_groq/requirement.txt`.
4. Start the API with `uvicorn app.main:app --reload`.

Uploaded contracts are stored locally and their extracted text and analysis
are saved in MongoDB. Treat uploads and AI-generated analysis as sensitive;
the analysis is informational and is not legal advice.

### Kitab Exchange

Set `KITAB_API_KEY` in the shell before starting the API. For example, in
PowerShell:

```powershell
$env:KITAB_API_KEY = "replace-with-a-long-random-value"
uvicorn main:app --reload
```

Send that value in the `X-API-Key` header for protected user/book write
operations. The application stores data in a local SQLite database.

## Example endpoints

- **Foundation:** `GET /`, `GET /about`, `GET /orders`, and
  `GET /debug/request-info`.
- **ChaiPoint:** `GET /menu?category=chai`, optionally with
  `available_only=true`, and `GET /menu/{item_id}`.
- **PIN lookup:** `GET /pincode/{code}` and `POST /pincode/bulk`; `pincode-api/`
  also supports `POST /pincode/lookup`.
- **Pizza stock:** `POST /order/` and `GET /order/stock?id={id}`.
- **Rangmanch-1:** `POST /reviews/`, `GET /reviews/`, `GET /reviews/average/{play_name}`,
  `PATCH /reviews/{review_id}`, and `DELETE /reviews/{review_id}`.
- **Tiffin delivery:** `POST /orders/`, `GET /orders/`, `PATCH /orders/{order_id}`,
  and `GET /stats/daily`.
- **Kitab Exchange:** `GET /books/`, `POST /books/`, `PATCH /books/{book_id}`,
  `PATCH /books/{book_id}/sold`, and user endpoints under `/users/`.
- **RAG API:** `POST /query/` with a JSON body such as
  `{"question": "What does the document say?"}`.
- **Wakeel:** `POST /contracts/upload`, `GET /contracts/list`,
  `POST /analysis/{contract_id}`, and analysis retrieval under `/analysis/`.

## Local files and secrets

- `.env` files are ignored at every directory level. Only `.env.example`
  templates belong in Git; never put real credentials in a template.
- Local `.db`, `.sqlite`, `.sqlite3`, and `.pdf` files and contract upload
  directories are ignored. Add only non-sensitive fixtures that you have the
  right to distribute.
- Do not commit API keys, database passwords, uploaded contracts, or local
  database contents.

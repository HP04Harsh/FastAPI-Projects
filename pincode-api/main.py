# main.py — Indian PIN Code Lookup API with Custom Handlers + Bulk POST
from fastapi import FastAPI
from data import PINCODE_DB
from models import (
    PinCodeRequest,
    LocationResponse,
    BulkRequest,
    BulkResponse,
)
from exceptions import (
    PinCodeNotFoundError,
    InvalidPinCodeError,
    pincode_not_found_handler,
    invalid_pincode_handler,
)

app = FastAPI(
    title="Indian PIN Code Lookup API",
    description="Auto-fill city, state & district from 6-digit Indian PIN code during D2C checkout.",
    version="1.0.0",
)

# ============================================================
# STEP 1: Register Custom Exception Handlers with FastAPI App!
# (Bina register kiye custom exceptions 500 Internal Server Error denge!)
# ============================================================
app.add_exception_handler(PinCodeNotFoundError, pincode_not_found_handler)
app.add_exception_handler(InvalidPinCodeError, invalid_pincode_handler)


@app.get("/")
def root():
    return {"message": "PIN Code Lookup API is running"}


# ============================================================
# STEP 2: POST /pincode/bulk — JSON Body Request (Multiple PINs)
# ⚠️ Always use @app.post for JSON Body (NOT @app.get!)
# ============================================================
@app.post("/pincode/bulk", response_model=BulkResponse)
def bulk_lookup(request: BulkRequest):
    results: list[dict] = []
    missing: list[str] = []

    for code in request.pincodes:
        if code in PINCODE_DB:
            results.append(PINCODE_DB[code])
        else:
            missing.append(code)

    return BulkResponse(
        found=len(results),
        not_found=len(missing),
        results=results,
        missing=missing,
    )


# ============================================================
# STEP 3: POST /pincode/lookup — Single Lookup via JSON Body (Pydantic 422)
# ============================================================
@app.post("/pincode/lookup", response_model=LocationResponse)
def lookup_pincode_body(request: PinCodeRequest):
    if request.pincode not in PINCODE_DB:
        raise PinCodeNotFoundError(request.pincode)
    return PINCODE_DB[request.pincode]


# ============================================================
# STEP 4: GET /pincode/{code} — Single Lookup via Path Param (Custom 400/404)
# ============================================================
@app.get("/pincode/{code}", response_model=LocationResponse)
def lookup_pincode_path(code: str):
    # Path param pe Pydantic model nahi hai, toh custom exception raise karo!
    if len(code) != 6 or not code.isdigit():
        raise InvalidPinCodeError(code, "Must be exactly 6 numeric digits")

    if code not in PINCODE_DB:
        raise PinCodeNotFoundError(code)

    return PINCODE_DB[code]
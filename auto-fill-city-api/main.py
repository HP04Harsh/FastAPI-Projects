from fastapi import FastAPI
from data import pin_code_db
from models import LocationResponse, BulkRequest, BulkResponse
from exceptions import (
    PinCodeNotFoundError,
    InvalidPinCodeError,
    pin_code_not_found_handler,
    invalid_pin_code_handler
)

app = FastAPI(title="PIN Code Lookup API")

# 1. Register Custom Exception Handlers
app.add_exception_handler(PinCodeNotFoundError, pin_code_not_found_handler)
app.add_exception_handler(InvalidPinCodeError, invalid_pin_code_handler)


# 2. Path Parameter Endpoint (GET Single)
@app.get("/pincode/{code}", response_model=LocationResponse)
def lookup_pincode(code: str):
    # Format Check
    if len(code) != 6 or not code.isdigit():
        raise InvalidPinCodeError(pin_code=code, reason="Must be exactly 6 numeric digits")

    # DB Lookup
    if code not in pin_code_db:
        raise PinCodeNotFoundError(pin_code=code)

    data = pin_code_db[code]
    return LocationResponse(
        pin_code=code,
        city=data["city"],
        state=data["state"],
        district=data["district"]
    )


# 3. Request Body Endpoint (POST Bulk)
@app.post("/pincode/bulk", response_model=BulkResponse)
def bulk_lookup(request: BulkRequest):
    results = []
    missing = []

    for code in request.pin_codes:
        if code in pin_code_db:
            data = pin_code_db[code]
            results.append(
                LocationResponse(
                    pin_code=code,
                    city=data["city"],
                    state=data["state"],
                    district=data["district"]
                )
            )
        else:
            missing.append(code)

    return BulkResponse(
        found=len(results),
        not_found=len(missing),
        results=results,
        missing=missing
    )

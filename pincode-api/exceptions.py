# exceptions.py — Production-Grade Custom Exception Classes + Handlers
from fastapi import Request
from fastapi.responses import JSONResponse


# ============================================================
# PART 1: Custom Exception Classes (Inherit from Python Exception)
# ============================================================
class PinCodeNotFoundError(Exception):
    """Jab valid 6-digit PIN code hamare database me nahi mile."""
    def __init__(self, pincode: str):
        self.pincode = pincode


class InvalidPinCodeError(Exception):
    """Jab PIN code ka format galat ho (length != 6 ya non-digit)."""
    def __init__(self, pincode: str, reason: str = "Invalid format"):
        self.pincode = pincode
        self.reason = reason


# ============================================================
# PART 2: Custom Exception Handlers (Return explicit JSONResponse!)
# Note: Regular routes me FastAPI dict -> JSON auto karta hai,
# par custom exception handlers me manually JSONResponse return karna padta hai!
# ============================================================
async def pincode_not_found_handler(
    request: Request, exc: PinCodeNotFoundError
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "error": "PINCODE_NOT_FOUND",
            "message": f"No location found for PIN code '{exc.pincode}'",
            "pincode": exc.pincode,
        },
    )


async def invalid_pincode_handler(
    request: Request, exc: InvalidPinCodeError
) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={
            "error": "INVALID_PINCODE",
            "message": f"PIN code '{exc.pincode}' is invalid: {exc.reason}",
            "pincode": exc.pincode,
        },
    )
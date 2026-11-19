from fastapi import Request
from fastapi.responses import JSONResponse

class PinCodeNotFoundError(Exception):
    def __init__(self, pin_code: str):
        self.pin_code = pin_code

class InvalidPinCodeError(Exception):
    def __init__(self, pin_code: str, reason: str = "Invalid format"):
        self.pin_code = pin_code
        self.reason = reason

async def pin_code_not_found_handler(request: Request, exc: PinCodeNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "PINCODE_NOT_FOUND",
            "message": f"No location found for PIN code '{exc.pin_code}'",
            "pin_code": exc.pin_code
        }
    )

async def invalid_pin_code_handler(request: Request, exc: InvalidPinCodeError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "INVALID_PINCODE",
            "message": f"PIN code '{exc.pin_code}' is invalid: {exc.reason}",
            "pin_code": exc.pin_code
        }
    )

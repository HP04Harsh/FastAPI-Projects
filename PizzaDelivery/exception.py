
class OutOfStock(Exception):
    def __init__(self,pizza):
        self.pizza = pizza

class PinCodeNotFoundError(Exception):
    def __init__(self, pin_code: str):
        self.pin_code = pin_code        


async def pin_code_not_found_handler(request: Request, exc: PinCodeNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "error": "PINCODE_NOT_FOUND",
            "message": f"No location found for PIN code '{exc.pin_code}'",
            "pin_code": exc.pin_code
        }
    )

async def out_of_stock_handler(request:Request, exc: OutOfStock):
    return JSONResponse(
        status_code=401,
        content={
            "error" : "Out Of Stock Error",
            "message" : f"stock of '{exc.pizza}' is empty",
            "pizza": exc.pizza 
        }
    )
       
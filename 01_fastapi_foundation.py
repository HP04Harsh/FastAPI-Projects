from fastapi import FastAPI,Request

app = FastAPI(
    title="Swiggy Order Service API",
    description="Internal API to handle order creation, listing & metadata.",
    version="1.2.2",
    docs_url="/docs",       # Swagger UI (Try it out interactive docs)
    redoc_url="/redoc",     # ReDoc (Clean reading docs)
)

#  Root / Health check route
@app.get("/", tags=["Health"])
def read_root():
    """Health check endpoint."""
    return {
        "message": "Welcome to Swiggy Order Service",
        "status": "healthy",
    }

# API Metadata route
@app.get("/about", tags=["Health"])
def about():
    """Returns API metadata."""
    return {
        "service": "order-service",
        "team": "backend-platform",
        "region": "ap-south-1",
        "version": "1.2.2",
    }    

@app.get("/orders", tags=["Orders"])
def list_orders():
    """List recent orders."""
    return {
        "orders": [
            {"id": 1, "item": "Butter Chicken", "status": "delivered"},
            {"id": 2, "item": "Masala Dosa", "status": "delivered"},
            {"id": 3, "item": "Paneer Tikka", "status": "preparing"},
        ]
    }


@app.get("/orders/status", tags=["Orders"])
def order_status():
    """Get order status summary for admin."""
    return {
        "total_today": 340_233,  # Python me underscore readability ke liye valid hai!
        "top_city": "Bengaluru",
    }    


@app.get(
    "/orders/active",
    summary="Get active orders",
    description="Returns all orders that are currently being prepared in kitchens.",
    tags=["Orders"],
)
def active_orders():
    return {
        "active_orders": [
            {"id": 3, "item": "Paneer Tikka", "status": "preparing"},
        ]
    }


@app.get("/debug/request-info", tags=["Debug"])
async def request_info(request: Request):
    """Inspect the raw incoming HTTP Request object."""
    return {
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "path_params": request.path_params,
        "query_params": dict(request.query_params),
    }
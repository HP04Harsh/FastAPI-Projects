from fastapi import FastAPI, HTTPException, Query
from data import menu_items
from models import MenuItem, MenuResponse

app = FastAPI(
    title="ChaiPoint Menu API",
    description="Read-only menu API for Bengaluru Kiosk displays and mobile apps.",
    version="1.0.0",
)


@app.get("/")
def root():
    """Welcome / health endpoint."""
    return {"message": "Welcome to ChaiPoint Menu API"}


# 1. GET /menu — List all items OR filter by ?category=chai (Query Parameter)
@app.get("/menu", response_model=MenuResponse)
def get_menu(
    category: str | None = Query(
        default=None,
        description="Filter items by category: chai, snacks, or combos",
    ),
    available_only: bool = Query(
        default=False,
        description="Set true to return only currently available items",
    ),
):
    filtered = menu_items

    # Category filter (case-insensitive using .lower()!)
    if category:
        filtered = [
            item for item in filtered
            if item["category"].lower() == category.lower()
        ]
        if not filtered:
            raise HTTPException(
                status_code=404,
                detail=f"No items found in category '{category}'",
            )

    # Optional availability filter
    if available_only:
        filtered = [item for item in filtered if item["available"]]

    return MenuResponse(
        count=len(filtered),
        items=filtered,
    )


# 2. GET /menu/{item_id} — Dynamic Path Parameter (FastAPI auto-casts to int!)
@app.get("/menu/{item_id}", response_model=MenuItem)
def get_menu_item(item_id: int):
    for item in menu_items:
        if item["id"] == item_id:
            return item

    # Loop khatam hua aur item nahi mila -> 404 HTTPException!
    raise HTTPException(
        status_code=404,
        detail=f"Menu item with ID {item_id} not found",
    )
from pydantic import BaseModel


class MenuItem(BaseModel):
    """Ek single ChaiPoint menu item ka exact shape."""
    id: int
    name: str
    category: str
    price: float
    description: str
    available: bool


class MenuResponse(BaseModel):
    """Standardized response envelope — har /menu call pe same format!"""
    status: str = "success"     # Default value 'success'
    count: int                  # Kitne items return ho rahe hain
    items: list[MenuItem]       # MenuItem objects ki list
from pydantic import BaseModel, field_validator

# --- Single Response Model ---
class LocationResponse(BaseModel):
    pin_code: str
    city: str
    state: str
    district: str

# --- Bulk Search Request & Validator ---
class BulkRequest(BaseModel):
    pin_codes: list[str]

    @field_validator("pin_codes")
    @classmethod
    def validate_pin_codes(cls, values: list[str]) -> list[str]:
        if len(values) == 0:
            raise ValueError("At least one PIN code is required")
        if len(values) > 20:
            raise ValueError("Maximum 20 PIN codes allowed per request")

        for code in values:
            if len(code) != 6 or not code.isdigit():
                raise ValueError(f"PIN code '{code}' must be exactly 6 numeric digits")

        return values

# --- Bulk Search Response Model ---
class BulkResponse(BaseModel):
    status: str = "success"
    found: int
    not_found: int
    results: list[LocationResponse]
    missing: list[str]

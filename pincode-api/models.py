# models.py — Pydantic @field_validator for Indian 6-Digit PIN Codes
from pydantic import BaseModel, field_validator


class PinCodeRequest(BaseModel):
    pincode: str

    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, value: str) -> str:
        # Indian PIN code strictly 6 digits ka hota hai (no letters/spaces)
        if len(value) != 6 or not value.isdigit():
            raise ValueError("PIN code must be exactly 6 digits")
        # ⚠️ KABHI MAT BHOOLNA: return value zaroor likhna!
        return value


class LocationResponse(BaseModel):
    pincode: str
    city: str
    state: str
    district: str


class BulkRequest(BaseModel):
    pincodes: list[str]

    @field_validator("pincodes")
    @classmethod
    def validate_pincodes(cls, values: list[str]) -> list[str]:
        if len(values) == 0:
            raise ValueError("At least one PIN code is required")
        if len(values) > 20:
            raise ValueError("Maximum 20 PIN codes allowed per request")
        for code in values:
            if len(code) != 6 or not code.isdigit():
                raise ValueError(
                    f"Invalid PIN code '{code}': each PIN code must be exactly 6 digits"
                )
        return values


class BulkResponse(BaseModel):
    status: str = "success"
    found: int
    not_found: int
    results: list[LocationResponse]
    missing: list[str]
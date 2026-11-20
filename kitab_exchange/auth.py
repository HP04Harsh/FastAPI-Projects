import hmac
import os

from fastapi import Header, HTTPException, status

API_KEY = os.getenv("KITAB_API_KEY")

def verify_api_key(x_api_key: str = Header(...)):
    """
    Extracts 'X-API-Key' from incoming request headers
    and validates it against the internal secret.
    """
    if not API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="API key authentication is not configured",
        )

    if not hmac.compare_digest(x_api_key, API_KEY):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing X-API-Key header"
        )
    return x_api_key
from typing import List
import httpx

from app.config import CURRENCY_API_KEY
from app.models import CurrencyRateModel
from app.services.cache import get_from_cache, set_to_cache


async def fetch_currency_rates(base_currency: str) -> List[CurrencyRateModel]:
    """Fetches currency exchange rates for major target currencies."""
    base = base_currency.upper()
    cache_key = f"currency:{base}"
    cached_data = get_from_cache(cache_key)
    if cached_data:
        return cached_data

    target_currencies = ["USD", "EUR", "GBP", "INR", "AED"]
    url = f"https://v6.exchangerate-api.com/v6/{CURRENCY_API_KEY}/latest/{base}"

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)

        if response.status_code == 200:
            rates_data = response.json().get("conversion_rates", {})
            result = []
            for target in target_currencies:
                if target in rates_data:
                    result.append(
                        CurrencyRateModel(
                            target_currency=target,
                            exchange_rate=float(rates_data[target])
                        )
                    )
            set_to_cache(cache_key, result, ttl_seconds=3600)  # 1 Hour Cache
            return result

    except Exception:
        pass

    # Fallback Mock Exchange Rates
    mock_rates = [
        CurrencyRateModel(target_currency="USD", exchange_rate=0.012 if base == "INR" else 1.0),
        CurrencyRateModel(target_currency="EUR", exchange_rate=0.011 if base == "INR" else 0.92),
        CurrencyRateModel(target_currency="INR", exchange_rate=1.0 if base == "INR" else 83.50)
    ]
    set_to_cache(cache_key, mock_rates, ttl_seconds=3600)
    return mock_rates
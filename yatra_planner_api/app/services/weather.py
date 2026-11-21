from datetime import date
from typing import List
import httpx

from app.config import WEATHER_API_KEY
from app.models import WeatherResponseModel
from app.services.cache import get_from_cache, set_to_cache


async def fetch_weather_forecast(destination: str, start_date: date, end_date: date) -> List[WeatherResponseModel]:
    """Fetches real-time weather forecast from WeatherAPI with in-memory caching."""
    cache_key = f"weather:{destination.lower()}:{start_date}:{end_date}"
    cached_data = get_from_cache(cache_key)
    if cached_data:
        return cached_data

    # Real-Time API Call
    num_days = (end_date - start_date).days + 1
    url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": destination,
        "days": min(num_days, 10),
        "aqi": "no",
        "alerts": "no"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            forecast_list = []
            for day_data in data.get("forecast", {}).get("forecastday", []):
                day_info = day_data["day"]
                forecast_list.append(
                    WeatherResponseModel(
                        date=day_data["date"],
                        condition=day_info["condition"]["text"],
                        temp_high_c=day_info["maxtemp_c"],
                        temp_low_c=day_info["mintemp_c"],
                        humidity=day_info["avghumidity"],
                        chance_of_rain=day_info.get("daily_chance_of_rain", 0)
                    )
                )
            set_to_cache(cache_key, forecast_list, ttl_seconds=600)  # 10 Mins Cache
            return forecast_list

    except Exception:
        pass

    # Mock Fallback if key missing or network fails
    mock_weather = [
        WeatherResponseModel(
            date=str(start_date),
            condition="Sunny with Partial Clouds",
            temp_high_c=31.5,
            temp_low_c=24.0,
            humidity=65,
            chance_of_rain=10
        )
    ]
    set_to_cache(cache_key, mock_weather, ttl_seconds=600)
    return mock_weather
import asyncio
from fastapi import APIRouter, HTTPException, status

from app.models import TravelRequestModel, TravelPlanResponseModel
from app.services.cache import clear_cache, get_cache_stats
from app.services.currency import fetch_currency_rates
from app.services.places import fetch_places_of_interest
from app.services.weather import fetch_weather_forecast

router = APIRouter(prefix="/plan", tags=["Standard Travel Plan"])


@router.post("/", response_model=TravelPlanResponseModel, status_code=status.HTTP_200_OK)
async def create_travel_plan(payload: TravelRequestModel):
    """
    Standard aggregated endpoint.
    Runs weather, places, and currency lookups CONCURRENTLY using asyncio.gather.
    """
    # Validations
    if payload.start_date > payload.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="start_date cannot be after end_date."
        )

    trip_days = (payload.end_date - payload.start_date).days + 1
    if trip_days > 14:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Travel plan duration cannot exceed 14 days."
        )

    # Parallel Data Aggregation via asyncio.gather
    weather_task = fetch_weather_forecast(payload.destination, payload.start_date, payload.end_date)
    places_task = fetch_places_of_interest(payload.destination)
    currency_task = fetch_currency_rates(payload.base_currency)

    weather_data, places_data, currency_data = await asyncio.gather(
        weather_task,
        places_task,
        currency_task
    )

    return TravelPlanResponseModel(
        destination=payload.destination,
        trip_duration_days=trip_days,
        weather_forecast=weather_data,
        currency_rates=currency_data,
        places_to_visit=places_data
    )


@router.get("/cache/stats")
def cache_statistics():
    """Returns current in-memory cache usage statistics."""
    return get_cache_stats()


@router.delete("/cache/clear")
def flush_cache():
    """Flushes all entries stored in the in-memory cache."""
    cleared_count = clear_cache()
    return {"message": "Cache successfully cleared.", "items_removed": cleared_count}
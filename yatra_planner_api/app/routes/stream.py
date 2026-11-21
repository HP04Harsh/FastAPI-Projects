import json
from datetime import date
from typing import AsyncGenerator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.models import TravelRequestModel
from app.services.currency import fetch_currency_rates
from app.services.places import fetch_places_of_interest
from app.services.weather import fetch_weather_forecast

router = APIRouter(prefix="/plan", tags=["Streaming Travel Plan (SSE)"])


def format_sse(event: str, data: dict) -> str:
    """
    Formats dictionary into valid Server-Sent Events (SSE) string frame:
    event: <event_name>
    data: <json_string>
    \n\n
    """
    # JSON Encoder for pydantic models and dates
    json_payload = json.dumps(data, default=lambda o: o.model_dump() if hasattr(o, "model_dump") else str(o))
    return f"event: {event}\ndata: {json_payload}\n\n"


async def travel_plan_generator(payload: TravelRequestModel) -> AsyncGenerator[str, None]:
    """Async Generator yielding SSE events progressively as data fetches complete."""

    # 1. Step 1: Initial Event
    yield format_sse("start", {
        "message": f"Aggregating travel plan for {payload.destination}",
        "status": "in_progress"
    })

    # 2. Step 2: Stream Weather
    weather_data = await fetch_weather_forecast(payload.destination, payload.start_date, payload.end_date)
    yield format_sse("weather", {
        "status": "ready",
        "data": weather_data
    })

    # 3. Step 3: Stream Places
    places_data = await fetch_places_of_interest(payload.destination)
    yield format_sse("places", {
        "status": "ready",
        "data": places_data
    })

    # 4. Step 4: Stream Currency
    currency_data = await fetch_currency_rates(payload.base_currency)
    yield format_sse("currency", {
        "status": "ready",
        "data": currency_data
    })

    # 5. Step 5: Complete Event
    yield format_sse("complete", {
        "message": "All travel plan data successfully aggregated.",
        "status": "finished"
    })


@router.post("/stream")
async def stream_travel_plan(payload: TravelRequestModel):
    """
    Server-Sent Events (SSE) streaming endpoint.
    Emits chunked JSON updates progressively over a single connection (`Content-Type: text/event-stream`).
    """
    if payload.start_date > payload.end_date:
        raise HTTPException(status_code=400, detail="start_date cannot be after end_date.")

    return StreamingResponse(
        travel_plan_generator(payload),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Prevents Nginx response buffering
        }
    )
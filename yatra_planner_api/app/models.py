from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field


class TravelRequestModel(BaseModel):
    destination: str = Field(..., example="Goa")
    start_date: date = Field(..., example="2026-04-01")
    end_date: date = Field(..., example="2026-04-05")
    base_currency: str = Field(default="INR", example="INR")


class WeatherResponseModel(BaseModel):
    date: str
    condition: str
    temp_high_c: float
    temp_low_c: float
    humidity: int
    chance_of_rain: int


class PlaceOfInterestModel(BaseModel):
    name: str
    description: str
    category: str
    rating: float
    estimated_hours: float
    entry_fee_inr: Optional[float] = 0.0



class CurrencyRateModel(BaseModel):
    target_currency: str
    exchange_rate: float



class TravelPlanResponseModel(BaseModel):
    destination: str
    trip_duration_days: int
    weather_forecast: List[WeatherResponseModel]
    currency_rates: List[CurrencyRateModel]
    places_to_visit: List[PlaceOfInterestModel]
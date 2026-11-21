import os
from dotenv import load_dotenv

load_dotenv()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "demo_weather_key")
CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY", "demo_currency_key")
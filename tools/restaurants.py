from langchain_core.tools import tool
from pydantic import BaseModel, Field
import requests
import os

TRIPADVISOR_API_KEY = os.environ["TRIPADVISOR_API_KEY"]

class RestaurantSearchInput(BaseModel):
    location_name: str = Field(description="City or location name")
    latitude: float = Field(description="Latitude of the location")
    longitude: float = Field(description="Longitude of the location")
    radius: int = Field(default=10, description="Search radius in kilometers from the given coordinates")

@tool(
    "RestaurantSearch",
    description="Search for restaurants in a given location using TripAdvisor API.",
    args_schema=RestaurantSearchInput
)
def search_restaurants(location_name: str, latitude: float, longitude: float, radius: int = 10):
    url = f"https://api.content.tripadvisor.com/api/v1/location/search"
    params = {
        "key": TRIPADVISOR_API_KEY,
        "searchQuery": location_name,
        "latLong": f"{latitude},{longitude}",
        "radius": radius,
        "radiusUnit": "km",
        "category": "restaurants",
        "language": "pl"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return {"error": response.text}
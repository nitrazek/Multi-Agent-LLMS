import requests
import os
from pydantic import BaseModel, Field

TRIPADVISOR_API_KEY = os.environ["TRIPADVISOR_API_KEY"]

class NearbySearchInput(BaseModel):
    latitude: float = Field(description="Latitude of the location")
    longitude: float = Field(description="Longitude of the location")
    radius: int = Field(description="Radius in kilometers around location in which to search for")

def send_nearby_search_request(category: str, latitude: float, longitude: float, radius: int):
    url = f"https://api.content.tripadvisor.com/api/v1/location/nearby_search"
    params = {
        "key": TRIPADVISOR_API_KEY,
        "latLong": f"{latitude},{longitude}",
        "radius": radius,
        "radiusUnit": "km",
        "category": category,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return { "error": response.text }

from langchain_core.tools import tool
from pydantic import BaseModel, Field
import requests
import os

TRIPADVISOR_API_KEY = os.environ["TRIPADVISOR_API_KEY"]

class POISearchInput(BaseModel):
    location: str = Field(description="City or location name")

@tool(
    "POISearch",
    description="Search for points of interest (attractions) in a given location using TripAdvisor API.",
    args_schema=POISearchInput
)
def search_poi(location: str):
    url = f"https://api.content.tripadvisor.com/api/v1/location/search"
    params = {
        "key": TRIPADVISOR_API_KEY,
        "searchQuery": location,
        "category": "attractions",
        "language": "pl"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return {"error": response.text}
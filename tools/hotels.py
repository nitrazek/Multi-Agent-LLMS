from langchain_core.tools import tool
from pydantic import BaseModel, Field
import requests
import os

TRIPADVISOR_API_KEY = os.environ["TRIPADVISOR_API_KEY"]

class HotelSearchInput(BaseModel):
    location: str = Field(description="City or location name")

@tool(
    "HotelSearch",
    description="Search for hotels in a city and return the best options.",
    args_schema=HotelSearchInput
)
def search_hotels(location: str):
    url = f"https://api.content.tripadvisor.com/api/v1/location/search"
    params = {
        "key": TRIPADVISOR_API_KEY,
        "searchQuery": location,
        "category": "hotels",
        "language": "pl"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return {"error": response.text}
from langchain_core.tools import tool
from pydantic import BaseModel, Field
from geopy.geocoders import Nominatim

user_agent = "travel-agent"

class GeocodeInput(BaseModel):
    query: str = Field(description="The address to geocode.")

@tool(
    "Geocoder",
    description="Geocode an address or location name to latitude and longitude (None if not found).",
    args_schema=GeocodeInput
)
async def geocode(query: str) -> tuple[float, float] | None:
    geolocator = Nominatim(user_agent=user_agent)
    location = geolocator.geocode(query, exactly_one=True)
    if location:
        return (location.latitude, location.longitude)
    return None

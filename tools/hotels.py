from langchain_core.tools import tool
from tools.api.tripadvisor import NearbySearchInput, send_nearby_search_request

@tool(
    "HotelSearch",
    description="Search for hotels in a city and return the best options.",
    args_schema=NearbySearchInput
)
def search_hotels(latitude: float, longitude: float, radius: int):
    return send_nearby_search_request(
        category="hotels",
        latitude=latitude,
        longitude=longitude,
        radius=radius
    )

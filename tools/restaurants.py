from langchain_core.tools import tool
from tools.api.tripadvisor import NearbySearchInput, send_nearby_search_request

@tool(
    "RestaurantSearch",
    description="Search for restaurants in a given location using TripAdvisor API.",
    args_schema=NearbySearchInput
)
def search_restaurants(latitude: float, longitude: float, radius: int):
    return send_nearby_search_request(
        category="restaurants",
        latitude=latitude,
        longitude=longitude,
        radius=radius
    )

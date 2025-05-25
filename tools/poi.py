from langchain_core.tools import tool
from tools.api.tripadvisor import NearbySearchInput, send_nearby_search_request

@tool(
    "POISearch",
    description="Search for points of interest (attractions) in a given location using TripAdvisor API.",
    args_schema=NearbySearchInput
)
def search_poi(latitude: float, longitude: float, radius: int):
    return send_nearby_search_request(
        category="attractions",
        latitude=latitude,
        longitude=longitude,
        radius=radius
    )

from langchain_core.tools import tool
from pydantic import BaseModel, Field
from amadeus import Client, ResponseError
import os

amadeus = Client(
    client_id=os.environ["AMADEUS_CLIENT_ID"],
    client_secret=os.environ["AMADEUS_CLIENT_SECRET"]
)

class FlightSearchInput(BaseModel):
    origin: str = Field(description="IATA code of the origin airport")
    destination: str = Field(description="IATA code of the destination airport")
    departure_date: str = Field(description="Departure date in YYYY-MM-DD format")
    return_date: str | None = Field(default=None, description="Return date in YYYY-MM-DD format (optional)")

@tool(
    "FlightSearch",
    description="Search for available flights between two airports and return the cheapest options.",
    args_schema=FlightSearchInput
)
def search_flights(origin: str, destination: str, departure_date: str, return_date: str = None):
    try:
        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": departure_date,
            "adults": 1,
            "currencyCode": "PLN",
            "max": 3
        }
        if return_date:
            params["returnDate"] = return_date
        response = amadeus.shopping.flight_offers_search.get(**params)
        return response.data
    except ResponseError as e:
        return {"error": str(e)}
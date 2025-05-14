from langchain_core.tools import tool
from pydantic import BaseModel, Field
from amadeus import Client, ResponseError
import os

amadeus = Client(
    client_id=os.environ["AMADEUS_CLIENT_ID"],
    client_secret=os.environ["AMADEUS_CLIENT_SECRET"]
)

class HotelSearchInput(BaseModel):
    city_code: str = Field(description="IATA city code (e.g. WAW for Warsaw)")
    check_in_date: str = Field(description="Check-in date in YYYY-MM-DD format")
    check_out_date: str = Field(description="Check-out date in YYYY-MM-DD format")

@tool(
    "HotelSearch",
    description="Search for hotels in a city and return the best options.",
    args_schema=HotelSearchInput
)
def search_hotels(city_code: str, check_in_date: str, check_out_date: str):
    try:
        response = amadeus.shopping.hotel_offers.get(
            cityCode=city_code,
            checkInDate=check_in_date,
            checkOutDate=check_out_date,
            adults=1,
            roomQuantity=1,
            paymentPolicy="NONE",
            includeClosed=False,
            bestRateOnly=True,
            view="FULL",
            sort="PRICE"
        )
        return response.data
    except ResponseError as e:
        return {"error": str(e)}
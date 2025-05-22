from tools.hotels import search_hotels
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

hotel_agent_prompt = """
Jesteś agentem wyszukiwania hoteli.
Otrzymujesz dane dotyczące miejsca początkowego, docelowego oraz daty podróży
Twoje zadania to:
- znalezienie najlepszych dostępnych hoteli w miejscu docelowym w podanym terminie
Do wykonania zadań wykorzystaj narzędzie HotelSearch do wyszukiwania hoteli
"""

hotel_agent_output_prompt = """
Odpowiedz w poniższym formacie:
{
    hotels: <lista najlepszych hoteli> = [
        {
            name: <nazwa hotelu>,
            address: <adres hotelu>,
            price: <cena za noc>,
            rating: <ocena hotelu>
        },
        ...
    ]
}
"""

class HotelInfo(BaseModel):
    name: str
    address: str
    price: float
    rating: float

class HotelAgentResponse(BaseModel):
    hotels: list[HotelInfo]

def create_hotel_agent(ollama_llm):
    return create_react_agent(
        name="hotel_agent",
        model=ollama_llm,
        tools=[search_hotels],
        prompt=hotel_agent_prompt,
        response_format=(hotel_agent_output_prompt, HotelAgentResponse)
    )

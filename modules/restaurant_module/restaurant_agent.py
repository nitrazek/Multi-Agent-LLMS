from tools.restaurants import search_restaurants
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

restaurant_agent_prompt = """
Jesteś agentem wyszukiwania restauracji.
Otrzymujesz dane dotyczące miejsca początkowego, docelowego oraz daty podróży
Twoim zadania to:
- znalezienie najlepszych restauracji w miejscu docelowym w podanym terminie
Do wykonania zadań wykorzystaj narzędzie RestaurantSearch do wyszukiwania restauracji
"""

restaurant_agent_output_prompt = """
Odpowiedz w poniższym formacie:
{
    restaurants: <lista najlepszych restauracji> = [
        {
            name: <nazwa restauracji>,
            address: <adres restauracji>,
            cuisine: <typ kuchni>
            rating: <ocena restauracji>
        },
        ...
    ]
}
"""

class RestaurantInfo(BaseModel):
    name: str
    address: str
    cuisine: str
    rating: float

class RestaurantAgentResponse(BaseModel):
    restaurants: list[RestaurantInfo]

def create_restaurant_agent(ollama_llm):
    return create_react_agent(
        name="restaurant_agent",
        model=ollama_llm,
        tools=[search_restaurants],
        prompt=restaurant_agent_prompt,
        response_format=(restaurant_agent_output_prompt, RestaurantAgentResponse)
    )

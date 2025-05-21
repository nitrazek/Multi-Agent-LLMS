from tools.hotels import search_hotels
from langgraph.prebuilt import create_react_agent

hotel_agent_prompt = """
Jesteś agentem wyszukiwania hoteli.
Otrzymujesz dane dotyczące lokalizacji oraz dat pobytu.
Twoim zadaniem jest znaleźć najlepsze dostępne hotele w podanym terminie, korzystając z narzędzia HotelSearch.
Zwróć najważniejsze informacje: nazwa hotelu, lokalizacja, cena za noc, ocena.
"""

def create_hotel_agent(ollama_llm):
    return create_react_agent(
        name="hotel_agent",
        model=ollama_llm,
        tools=[search_hotels],
        prompt=hotel_agent_prompt
    )
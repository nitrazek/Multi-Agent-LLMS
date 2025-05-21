from tools.restaurants import search_restaurants
from langgraph.prebuilt import create_react_agent

restaurant_agent_prompt = """
Jesteś agentem wyszukiwania restauracji.
Otrzymujesz dane dotyczące lokalizacji.
Twoim zadaniem jest znaleźć najlepsze restauracje w danym miejscu, korzystając z narzędzia RestaurantSearch.
Zwróć najważniejsze informacje: nazwa, typ kuchni, ocena, adres.
"""

def create_restaurant_agent(ollama_llm):
    return create_react_agent(
        name="restaurant_agent",
        model=ollama_llm,
        tools=[search_restaurants],
        prompt=restaurant_agent_prompt
    )

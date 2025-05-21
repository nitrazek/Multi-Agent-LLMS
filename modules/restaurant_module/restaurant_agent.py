import os
from tools.restaurants import search_restaurants
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from modules.src.pre_model_hook import pre_model_hook

ollama_llm = ChatOllama(
    model=os.environ["OLLAMA_MODEL"],
    base_url=os.environ["OLLAMA_URL"],
)

restaurant_agent_prompt = """
Jesteś agentem wyszukiwania restauracji.
Otrzymujesz dane dotyczące lokalizacji.
Twoim zadaniem jest znaleźć najlepsze restauracje w danym miejscu, korzystając z narzędzia RestaurantSearch.
Zwróć najważniejsze informacje: nazwa, typ kuchni, ocena, adres.
"""

restaurant_agent = create_react_agent(
    name="restaurant_agent",
    model=ollama_llm,
    tools=[search_restaurants],
    prompt=restaurant_agent_prompt,
    pre_model_hook=pre_model_hook
)

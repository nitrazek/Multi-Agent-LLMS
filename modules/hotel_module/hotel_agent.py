import os
from tools.hotels import search_hotels
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

ollama_llm = ChatOllama(
    model=os.environ["OLLAMA_MODEL"],
    base_url=os.environ["OLLAMA_URL"],
)

hotel_agent_prompt = """
Jesteś agentem wyszukiwania hoteli.
Otrzymujesz dane dotyczące lokalizacji oraz dat pobytu.
Twoim zadaniem jest znaleźć najlepsze dostępne hotele w podanym terminie, korzystając z narzędzia HotelSearch.
Zwróć najważniejsze informacje: nazwa hotelu, lokalizacja, cena za noc, ocena.
"""

hotel_agent = create_react_agent(
    name="hotel_agent",
    model=ollama_llm,
    tools=[search_hotels],
    prompt=hotel_agent_prompt
)
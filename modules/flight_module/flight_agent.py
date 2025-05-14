import os
from tools.flights import search_flights
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

ollama_llm = ChatOllama(
    model=os.environ["OLLAMA_MODEL"],
    base_url=os.environ["OLLAMA_URL"],
)

flight_agent_prompt = """
Jesteś agentem wyszukiwania lotów.
Otrzymujesz dane dotyczące miejsca początkowego, docelowego oraz daty podróży.
Twoim zadaniem jest znaleźć najtańsze dostępne loty w podanym terminie, korzystając z narzędzia FlightSearch.
Zwróć najważniejsze informacje: linia lotnicza, godziny, cena, czas lotu.
"""

flight_agent = create_react_agent(
    name="flight_agent",
    model=ollama_llm,
    tools=[search_flights],
    prompt=flight_agent_prompt
)
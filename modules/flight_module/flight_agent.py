from tools.flights import search_flights
from langgraph.prebuilt import create_react_agent



flight_agent_prompt = """
Jesteś agentem wyszukiwania lotów.
Otrzymujesz dane dotyczące miejsca początkowego, docelowego oraz daty podróży.
Twoim zadaniem jest znaleźć najtańsze dostępne loty w podanym terminie, korzystając z narzędzia FlightSearch.
Zwróć najważniejsze informacje: linia lotnicza, godziny, cena, czas lotu.
"""

def create_flight_agent(ollama_llm):
    return create_react_agent(
        name="flight_agent",
        model=ollama_llm,
        tools=[search_flights],
        prompt=flight_agent_prompt
    )

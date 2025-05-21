from tools.flights import search_flights
from langgraph.prebuilt import create_react_agent

# flight_agent_prompt = """
# Jesteś agentem wyszukiwania lotów.
# Otrzymujesz dane dotyczące miejsca początkowego, docelowego oraz daty podróży w następującym formacie:
# - from: miejsce początkowe
# - from_coordinates: współrzędne miejsca docelowego
# - to: miejsce docelowe
# - to_coordinates: współrzędne miejsca docelowego
# - start_date: data początkowa
# - end_date: data końcowa
# Twoim zadaniem jest znaleźć najtańsze dostępne loty między miejscem początkowym a miejscem docelowym dla podanej daty początkowej, korzystając z narzędzia FlightSearch.
# Zwróć najważniejsze informacje: linia lotnicza, godziny, cena, czas lotu, lotnisko początkowe i lotnisko docelowe.
# """

flight_agent_prompt = """
Powiedz jak się nazywa stolica Polski.
"""

def create_flight_agent(ollama_llm):
    return create_react_agent(
        name="flight_agent",
        model=ollama_llm,
        tools=[search_flights],
        prompt=flight_agent_prompt
    )

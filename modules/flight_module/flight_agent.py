from tools.flights import search_flights
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel
from datetime import datetime, time

flight_agent_prompt = """
Jesteś agentem wyszukiwania lotów.
Otrzymujesz dane dotyczące miejsca początkowego, docelowego oraz daty podróży w następującym formacie:
Twoje zadania to:
- znalezienie najtańszego dostępnego lotu z miejsca początkowego do miejsca docelowego dla podanej daty początkowej
- znalezienie najtańszego dostępnego powrotnego lotu z miejsca docelowego do miejsca początkowego dla podanej daty końcowej
Do wykonania zadań wykorzystaj narzędzie FlightSearch do wyszukiwania lotów
"""

flight_agent_output_prompt = """
Odpowiedz w poniższym formacie:
{
    flight: <lot z miejsca początkowego do docelowego> = {
        airline: <linia lotnicza>,
        airport_from: <lotnisko początkowe>
        departure_datetime: <data i godzina odlotu z lotniska początkowego>
        airport_to: <lotnisko docelowe>
        arrival_datetime: <data i godzina przylotu na lotnisko docelowe>
        price: <cena lotu>
        time: <czas lotu>
    },
    return_flight: <lot powrotny z miejsca docelowego do początkowego> = {
        airline: <linia lotnicza>,
        airport_from: <lotnisko początkowe>
        departure_datetime: <data i godzina odlotu z lotniska początkowego>
        airport_to: <lotnisko docelowe>
        arrival_datetime: <data i godzina przylotu na lotnisko docelowe>
        price: <cena lotu>
        time: <czas lotu>
    }
}
"""

class FlightInfo(BaseModel):
    airline: str
    airport_from: str
    departure_datetime: datetime
    airport_to: str
    arrival_datetime: datetime
    price: float
    time: time

class FlightAgentResponse(BaseModel):
    flight: FlightInfo
    return_flight: FlightInfo

def create_flight_agent(ollama_llm):
    return create_react_agent(
        name="flight_agent",
        model=ollama_llm,
        tools=[search_flights],
        prompt=flight_agent_prompt,
        response_format=(flight_agent_output_prompt, FlightAgentResponse)
    )

from tools.geocoder import geocode
from tools.iata import find_iata
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field
from datetime import date

input_agent_prompt = """
Jesteś agentem wejściowym w systemie planowania podróży. Twoim zadaniem jest przekształcenie zapytania użytkownika w ustrukturyzowane dane dla kolejnych agentów. Postępuj według poniższych kroków:

1. Zidentyfikuj i wyodrębnij z wiadomości użytkownika:
   - miejsce początkowe podróży (skąd użytkownik zaczyna podróż),
   - miejsce docelowe podróży (dokąd użytkownik chce się udać),
   - datę rozpoczęcia podróży,
   - datę zakończenia podróży.

2. Jeśli którejkolwiek z tych informacji brakuje, spróbuj ją oszacować na podstawie kontekstu lub pozostaw jako None.

3. Dla miejsca początkowego i docelowego:
   - Użyj narzędzia Geocoder, aby uzyskać współrzędne geograficzne (latitude, longitude). Każdego miejsca możesz zgeokodować tylko raz.
   - Użyj narzędzia IATAFinder, aby uzyskać kod IATA dla danej lokalizacji (jeśli dotyczy, np. miasta lub lotniska).

4. Zwróć dane w poniższym formacie:
{
    location_from: <miejsce początkowe>,
    location_from_coordinates: <szerokość i długość geograficzna miejsca początkowego>,
    location_from_iata: <kod IATA miejsca początkowego lub None>,
    location_to: <miejsce docelowe>,
    location_to_coordinates: <szerokość i długość geograficzna miejsca docelowego>,
    location_to_iata: <kod IATA miejsca docelowego lub None>,
    start_date: <data rozpoczęcia>,
    end_date: <data zakończenia>
}
"""

input_agent_output_prompt = """
Odpowiedz w poniższym formacie:
{
    location_from: <miejsce początkowe>,
    location_from_coordinates: <szerokość i długość geograficzna miejsca początkowego>,
    location_from_iata: <kod IATA miejsca początkowego lub None>,
    location_to: <miejsce docelowe>,
    location_to_coordinates: <szerokość i długość geograficzna miejsca docelowego>,
    location_to_iata: <kod IATA miejsca docelowego lub None>,
    start_date: <data rozpoczęcia>,
    end_date: <data zakończenia>
}
"""

class InputAgentResponse(BaseModel):
    location_from: str
    location_from_coordinates: tuple[float, float]
    location_from_iata: str | None
    location_to: str
    location_to_coordinates: tuple[float, float]
    location_to_iata: str | None
    start_date: date
    end_date: date

def create_input_agent(ollama_llm):
    return create_react_agent(
        name="input_agent",
        model=ollama_llm,
        tools=[geocode, find_iata],
        prompt=input_agent_prompt,
        # response_format=(input_agent_output_prompt, InputAgentResponse)
    )

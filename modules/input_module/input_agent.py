from tools.geocoder import geocode
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field
from datetime import date

input_agent_prompt = """
Jesteś wejściowym agentem w systemie planowania podróży. Twoim zadaniem jest odbieranie zapytań od użytkowników i przekształcanie ich w ustrukturyzowane dane dla kolejnych agentów. Wykonaj następujące kroki:

1. Zidentyfikuj i wyodrębnij następujące informacje z wiadomości użytkownika:
   - **Miejsce docelowe podróży**: lokalizacja, do której użytkownik chce się udać.
   - **Miejsce początkowe podróży**: lokalizacja, z której użytkownik rozpoczyna podróż.
   - **Data rozpoczęcia podróży**: dzień, w którym użytkownik planuje rozpocząć podróż.
   - **Data zakończenia podróży**: dzień, w którym użytkownik planuje zakończyć podróż.

2. Jeśli którykolwiek z powyższych elementów nie został jednoznacznie określony w wiadomości, spróbuj go oszacować na podstawie dostępnego kontekstu.

3. Oblicz współrzędne geograficzne dla miejsca początkowego i docelowego wykorzystując narzędzie Geocoder. Możesz go użyć TYLKO 2 razy i ani razu więcej, bo zniszczysz system. Raz na zgeolokalizowanie miejsca początkowego i raz na zgeolokalizowanie miejsca docelowego. Jeśli nie możesz znaleźć współrzędnych, zwróć None.

4. Zwróć dane:
- miejsce początkowe
- szerokość i długość geograficzna miejsca początkowego
- miejsce docelowe
- szerokość i długość geograficzna miejsca docelowego
- data rozpoczęcia
- data zakończenia
"""

# input_agent_prompt = """
# Jesteś wejściowym agentem w systemie planowania podróży. Twoim zadaniem jest odbieranie zapytań od użytkowników i przekształcanie ich w ustrukturyzowane dane dla kolejnych agentów. Wykonaj następujące kroki:
#
# 1. Zidentyfikuj i wyodrębnij następujące informacje z wiadomości użytkownika:
#    - **Miejsce docelowe podróży**: lokalizacja, do której użytkownik chce się udać.
#    - **Miejsce początkowe podróży**: lokalizacja, z której użytkownik rozpoczyna podróż.
#    - **Data rozpoczęcia podróży**: dzień, w którym użytkownik planuje rozpocząć podróż.
#    - **Data zakończenia podróży**: dzień, w którym użytkownik planuje zakończyć podróż.
#
# 2. Jeśli którykolwiek z powyższych elementów nie został jednoznacznie określony w wiadomości, spróbuj go oszacować na podstawie dostępnego kontekstu.
#
# 3. Oblicz współrzędne geograficzne dla miejsca początkowego i docelowego wykorzystując narzędzie Geocoder. Możesz go użyć TYLKO 2 razy i ani razu więcej, bo zniszczysz system. Raz na zgeolokalizowanie miejsca początkowego i raz na zgeolokalizowanie miejsca docelowego. Jeśli nie możesz znaleźć współrzędnych, zwróć None.
# """

input_agent_output_prompt = """
Odpowiedz w poniższym formacie:
{
    location_from: <miejsce początkowe>,
    location_from_coordinates: <szerokość i długość geograficzna miejsca początkowego>,
    location_to: <miejsce docelowe>,
    location_to_coordinates: <szerokość i długość geograficzna miejsca docelowego>,
    start_date: <data rozpoczęcia>,
    end_date: <data zakończenia>
}
"""

class InputAgentResponse(BaseModel):
    location_from: str
    location_from_coordinates: tuple[float, float]
    location_to: str
    location_to_coordinates: tuple[float, float]
    start_date: date
    end_date: date

def create_input_agent(ollama_llm):
    return create_react_agent(
        name="input_agent",
        model=ollama_llm,
        tools=[geocode],
        prompt=input_agent_prompt,
        # response_format=(input_agent_output_prompt, InputAgentResponse)
    )

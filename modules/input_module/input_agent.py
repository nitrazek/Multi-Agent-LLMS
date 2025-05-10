import os
from tools.geocoder import geocode
from langchain_ollama import OllamaLLM
from langgraph.prebuilt import create_react_agent

ollama_llm = OllamaLLM(
  model=os.environ["OLLAMA_MODEL"],
  base_url=os.environ["OLLAMA_URL"],
)

input_agent_prompt = """
Jesteś wejściowym agentem w systemie planowania podróży i odpowiadasz na przyjmowanie zapytań od użytkowników.
Odbierz wiadomość od użytkownika dotyczącą planu podróży i wykonaj następujące kroki:

1. Zidentyfikuj i wyodrębnij cztery elementy:
   - Miejsce docelowe podróży
   - Miejsce początkowe podróży
   - Data rozpoczęcia podróży
   - Data zakończenia podróży

2. Jeśli którykolwiek z elementów nie został jednoznacznie określony, spróbuj go oszacować na podstawie kontekstu.

3. Przekaż wyodrębnione dane trzem agentom:
   - **FlightAgent**: podaj miejsce początkowe, miejsce docelowe, datę rozpoczęcia i zakończenia.
   - **HotelAgent**: podaj miejsce docelowe, datę rozpoczęcia i zakończenia.
   - **POIAgent**: podaj miejsce docelowe, datę rozpoczęcia i zakończenia.

Format przekazywanych danych do agentów:
```json
{
  "from": "<miejsce początkowe>",
  "to": "<miejsce docelowe>",
  "start_date": "<data rozpoczęcia>",
  "end_date": "<data zakończenia>"
}
"""

input_agent = create_react_agent(
    model=ollama_llm,
    tools=[geocode],
    prompt=input_agent_prompt
)

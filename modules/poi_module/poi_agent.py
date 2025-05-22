from tools.poi import search_poi
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

poi_agent_prompt = """
Jesteś agentem wyszukiwania atrakcji turystycznych.
Otrzymujesz dane dotyczące miejsca początkowego, docelowego oraz daty podróży
Twoje zadania to:
- znalezienie najciekawszych atrakcji do zwiedzania w miejscu docelowym w podanym terminie
Do wykonania zadań wykorzystaj narzędzie POISearch do wyszukiwania atrakcji
"""

poi_agent_output_prompt = """
Odpowiedz w poniższym formacie:
{
    attractions: <lista najlepszych atrakcji> = [
        {
            name: <nazwa atrakcji>,
            description: <opis atrakcji>,
            address: <adres hotelu>,
            price: <cena atrakcji lub 0 jest atrakcja jest darmowa>
        },
        ...
    ]
}
"""

class POIInfo(BaseModel):
    name: str
    description: str
    address: str
    price: float

class POIAgentResponse(BaseModel):
    attractions: list[POIInfo]

def create_poi_agent(ollama_llm):
    return create_react_agent(
        name="poi_agent",
        model=ollama_llm,
        tools=[search_poi],
        prompt=poi_agent_prompt,
        response_format=(poi_agent_output_prompt, POIAgentResponse)
    )

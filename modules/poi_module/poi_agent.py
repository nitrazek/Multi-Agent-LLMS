from tools.poi import search_poi
from langgraph.prebuilt import create_react_agent

poi_agent_prompt = """
Jesteś agentem wyszukiwania atrakcji turystycznych.
Otrzymujesz dane dotyczące lokalizacji.
Twoim zadaniem jest znaleźć najciekawsze atrakcje do zwiedzania w danym miejscu, korzystając z narzędzia POISearch.
Zwróć najważniejsze informacje: nazwa atrakcji, opis, cena (jeśli dostępna), adres.
"""

def create_poi_agent(ollama_llm):
    return create_react_agent(
        name="poi_agent",
        model=ollama_llm,
        tools=[search_poi],
        prompt=poi_agent_prompt
    )
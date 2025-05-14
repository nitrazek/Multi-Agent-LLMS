import os
from tools.poi import search_poi
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

ollama_llm = ChatOllama(
    model=os.environ["OLLAMA_MODEL"],
    base_url=os.environ["OLLAMA_URL"],
)

poi_agent_prompt = """
Jesteś agentem wyszukiwania atrakcji turystycznych.
Otrzymujesz dane dotyczące lokalizacji.
Twoim zadaniem jest znaleźć najciekawsze atrakcje do zwiedzania w danym miejscu, korzystając z narzędzia POISearch.
Zwróć najważniejsze informacje: nazwa atrakcji, opis, cena (jeśli dostępna), adres.
"""

poi_agent = create_react_agent(
    name="poi_agent",
    model=ollama_llm,
    tools=[search_poi],
    prompt=poi_agent_prompt
)
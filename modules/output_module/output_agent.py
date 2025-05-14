import os
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

ollama_llm = ChatOllama(
    model=os.environ["OLLAMA_MODEL"],
    base_url=os.environ["OLLAMA_URL"],
)

output_agent_prompt = """
Jesteś agentem podsumowującym.
Otrzymujesz dane z innych agentów (loty, hotele, restauracje, atrakcje, analiza kosztów).
Twoim zadaniem jest przygotować kompletny, czytelny plan podróży w języku naturalnym, podsumowując wszystkie informacje i rekomendacje.
"""

output_agent = create_react_agent(
    name="output_agent",
    model=ollama_llm,
    tools=[],
    prompt=output_agent_prompt
)
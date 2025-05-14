import os
from tools.charts import create_chart
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

ollama_llm = ChatOllama(
    model=os.environ["OLLAMA_MODEL"],
    base_url=os.environ["OLLAMA_URL"],
)

analytics_agent_prompt = """
Jesteś agentem analizy kosztów podróży.
Otrzymujesz dane o kosztach lotów, hoteli, atrakcji i restauracji.
Twoim zadaniem jest przygotować podsumowanie kosztów oraz wygenerować wykresy za pomocą narzędzia ChartTool.
Zwróć ścieżkę do wygenerowanego wykresu oraz krótkie podsumowanie.
"""

analytics_agent = create_react_agent(
    name="analytics_agent",
    model=ollama_llm,
    tools=[create_chart],
    prompt=analytics_agent_prompt
)
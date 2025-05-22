from tools.charts import create_chart
from langgraph.prebuilt import create_react_agent

analytics_agent_prompt = """
Jesteś agentem analizy kosztów podróży.
Otrzymujesz dane o kosztach w następujących kategoriach:
- loty
- hotele
- atrakcje
- restauracje
Twoim zadaniem jest przygotować podsumowanie kosztów dla każdej z tych kategorii oraz wygenerować wykres z przygotowanego podsumowania poprzez narzędzie ChartTool.
Zwróć odpowiedź w następującym formacie:
{
    [nazwa kategorii]: [łączna suma wydatków w danej kategorii],
    "chart_path": ścieżka do przygotowanego wykresu
}
"""

def create_analytics_agent(ollama_llm):
    return create_react_agent(
        name="analytics_agent",
        model=ollama_llm,
        tools=[create_chart],
        prompt=analytics_agent_prompt
    )

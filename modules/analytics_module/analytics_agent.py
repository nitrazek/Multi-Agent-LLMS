from tools.charts import create_chart
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

analytics_agent_prompt = """
Jesteś agentem analizy kosztów podróży.
Otrzymujesz dane dotyczące rekomendowanych lotów, hoteli, atrakcji i restauracji
Twoje zadania to:
- podsumowanie kosztów dla każdej z powyższych kategorii
- wygenerowanie wykresu kolumnowego z przygotowanego podsumowania
Do wykonania zadań wykorzystaj narzędzie ChartTool do generowania wykresów kolumnowych
"""

analytics_agent_output_prompt = """
Odpowiedz w poniższym formacie:
{
    flights_cost: <łączny koszt lotów>
    hotels_cost: <łączny koszt hoteli>
    attractions_cost: <łączny koszt atrakcji>
    restaurants_cost: <łączny koszt restauracji>
    chart_path: <ścieżka do wygenerowanego wykresu>
}
"""

class AnalyticsAgentResponse(BaseModel):
    flights_cost: float
    hotels_cost: float
    attractions_cost: float
    restaurants_cost: float
    chart_path: str

def create_analytics_agent(ollama_llm):
    return create_react_agent(
        name="analytics_agent",
        model=ollama_llm,
        tools=[create_chart],
        prompt=analytics_agent_prompt,
        response_format=(analytics_agent_output_prompt, AnalyticsAgentResponse)
    )
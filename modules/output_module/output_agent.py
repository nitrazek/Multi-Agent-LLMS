from langgraph.prebuilt import create_react_agent

output_agent_prompt = """
Jesteś agentem podsumowującym.
Otrzymujesz listę rekomendowanych lotów, hoteli, restauracji, atrakcji.
Twoim zadaniem jest przygotować kompletny, czytelny plan podróży w języku naturalnym, podsumowując wszystkie informacje i rekomendacje.
Przygotuj plan dla każdego dnia z podziałem na proponowane godziny.
"""

def create_output_agent(ollama_llm):
    return create_react_agent(
        name="output_agent",
        model=ollama_llm,
        tools=[],
        prompt=output_agent_prompt
    )

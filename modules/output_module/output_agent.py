from langgraph.prebuilt import create_react_agent

output_agent_prompt = """
Jesteś agentem podsumowującym.
Otrzymujesz dane z innych agentów (loty, hotele, restauracje, atrakcje, analiza kosztów).
Twoim zadaniem jest przygotować kompletny, czytelny plan podróży w języku naturalnym, podsumowując wszystkie informacje i rekomendacje.
"""

def create_output_agent(ollama_llm):
    return create_react_agent(
        name="output_agent",
        model=ollama_llm,
        tools=[],
        prompt=output_agent_prompt
    )
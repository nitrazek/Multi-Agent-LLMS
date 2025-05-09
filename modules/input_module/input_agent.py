import os
from tools.geocoder import geocode
from langchain_ollama import OllamaLLM
from langchain.agents import initialize_agent, AgentType

llm_llama = OllamaLLM(
  model=os.environ["OLLAMA_MODEL"],
  base_url=os.environ["OLLAMA_URL"],
)

agent = initialize_agent(
    tools=[geocode],
    llm=llm_llama,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)
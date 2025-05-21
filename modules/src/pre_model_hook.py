from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langchain_core.messages import RemoveMessage

def pre_model_hook(state: AgentState):
    last_message = state["messages"][-1] if len(state["messages"]) > 0 else None
    return { "messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES), last_message] }

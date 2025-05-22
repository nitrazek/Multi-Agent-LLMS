from langgraph.graph.message import REMOVE_ALL_MESSAGES
from langchain_core.messages import RemoveMessage, HumanMessage, AIMessage

def pre_model_hook(state):
    new_messages = state["messages"]+[HumanMessage(content="")] if not isinstance(state["messages"][-1], HumanMessage) else state["messages"]
    return { "llm_input_messages": new_messages }
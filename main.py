from dotenv import load_dotenv
load_dotenv(override=True)

import os
import click
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END, MessagesState
from modules.input_module.input_agent import create_input_agent
from modules.flight_module.flight_agent import create_flight_agent
from modules.hotel_module.hotel_agent import create_hotel_agent
from modules.restaurant_module.restaurant_agent import create_restaurant_agent
from modules.poi_module.poi_agent import create_poi_agent
from modules.analytics_module.analytics_agent import create_analytics_agent
from modules.output_module.output_agent import create_output_agent

from langgraph.pregel import Pregel
from langchain_core.messages import HumanMessage, ToolMessage, AIMessage
from langgraph.utils.runnable import RunnableCallable, RunnableConfig
import threading
import questionary

ollama_llm = ChatOllama(
    model=os.environ["OLLAMA_MODEL"],
    base_url=os.environ["OLLAMA_URL"]
)

# Inicjalizacja agentów
input_agent = create_input_agent(ollama_llm)
flight_agent = create_flight_agent(ollama_llm)
hotel_agent = create_hotel_agent(ollama_llm)
restaurant_agent = create_restaurant_agent(ollama_llm)
poi_agent = create_poi_agent(ollama_llm)
analytics_agent = create_analytics_agent(ollama_llm)
output_agent = create_output_agent(ollama_llm)

print_lock = threading.Lock()

class DebugLevel:
    STANDARD = "standard"
    VERBOSE = "verbose"
    SUPER_VERBOSE = "super verbose"

debug_level = DebugLevel.STANDARD

def set_debug_level():
    global debug_level
    click.clear()
    debug_level = questionary.select(
        "Wybierz poziom debugowania:",
        choices=[DebugLevel.STANDARD, DebugLevel.VERBOSE, DebugLevel.SUPER_VERBOSE],
        default=debug_level
    ).ask()

def print_state_messages(state):
    for message in state["messages"]:
        match message.__class__.__name__:
            case "HumanMessage":
                print(f"HUMAN -> {message.content}")
            case "AIMessage":
                print(f"AI ({message.name}) -> {message.content}")
            case "ToolMessage":
                print(f"TOOL ({message.name}) -> {message.content}")

def make_call_agent(agent: Pregel):
    def call_agent(state: dict, config: RunnableConfig) -> dict:
        output = agent.invoke({ **state, "messages": state["messages"] + [HumanMessage(content="")] })
        output["messages"] = [message for message in output["messages"] if not isinstance(message, HumanMessage) or message.content != ""]
        if output.get("structured_response") is not None:
            output["messages"] = output["messages"][:-1] + [AIMessage(content=output["structured_response"].model_dump_json(), name=agent.name)]
            del output["structured_response"]
        # Wypisz odpowiedź agenta zgodnie z poziomem debugowania
        if debug_level is DebugLevel.VERBOSE:
            with print_lock:
                print(f"\n=== {agent.name} ===")
                print_state_messages({"messages": [output["messages"][-1]]})
        elif debug_level is DebugLevel.SUPER_VERBOSE:
            with print_lock:
                print(f"\n=== {agent.name} ===")
                # Wypisz wszystkie nowe wiadomości (czyli te, które pojawiły się w output, a nie było ich w state)
                new_count = len(output["messages"]) - len(state["messages"])
                if new_count > 0:
                    print_state_messages({"messages": output["messages"][-new_count:]})
        output["messages"] = [message for message in output["messages"] if not isinstance(message, ToolMessage)]
        output["messages"] = [message for message in output["messages"] if not isinstance(message, AIMessage) or len(message.tool_calls) == 0]
        return output
    return RunnableCallable(call_agent)

# Definicja grafu multi-agentowego
multi_agent_graph = (
    StateGraph(MessagesState)
    # Input agent
    .add_node("input_agent", make_call_agent(input_agent))
    # Agenci równolegli (rekomendacje)
    .add_node("flight_agent", make_call_agent(flight_agent))
    .add_node("hotel_agent", make_call_agent(hotel_agent))
    .add_node("restaurant_agent", make_call_agent(restaurant_agent))
    .add_node("poi_agent", make_call_agent(poi_agent))
    # Analytics agent
    .add_node("analytics_agent", make_call_agent(analytics_agent))
    # Output agent
    .add_node("output_agent", make_call_agent(output_agent))
    # Przepływ: input -> równolegle 4 agentów -> analytics -> output
    .add_edge(START, "input_agent")
    .add_edge("input_agent", "flight_agent")
    .add_edge("input_agent", "hotel_agent")
    .add_edge("input_agent", "restaurant_agent")
    .add_edge("input_agent", "poi_agent")
    # Po zakończeniu wszystkich rekomendacji, przechodzimy do analytics
    .add_edge("flight_agent", "analytics_agent")
    .add_edge("hotel_agent", "analytics_agent")
    .add_edge("restaurant_agent", "analytics_agent")
    .add_edge("poi_agent", "analytics_agent")
    # Rekomendacje + analytics -> output
    .add_edge("analytics_agent", "output_agent")
    .compile()
)

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Interfejs CLI dla Multi-Agent-LLMS."""
    if not ctx.invoked_subcommand:
        menu()

@cli.command()
def menu():
    """Wyświetl menu główne."""
    while True:
        click.clear()
        click.echo("=== Multi-Agent-LLMS ===")
        click.echo("1. Zapytaj agenta o plan podróży")
        click.echo(f"2. Ustaw poziom debugowania (aktualnie: {debug_level})")
        click.echo("3. Wyjdź")
        choice = click.prompt("Wybierz opcję", type=int)

        if choice == 1:
            ask_agent()
        elif choice == 2:
            set_debug_level()
        elif choice == 3:
            click.echo("Do widzenia!")
            break
        else:
            click.echo("Nieprawidłowy wybór. Spróbuj ponownie.")

def ask_agent():
    """Zadaj pytanie agentowi."""
    click.clear()
    click.echo("=== Zapytaj agenta ===")
    question = click.prompt("Podaj pytanie (np. Zaplanuj podróż z Warszawy do Krakowa)")
    
    click.echo("\nAgenci myślą...")
    state = multi_agent_graph.invoke({ "messages": [{ "role": "user", "content": question }] })
    messages = state.get("messages")
    response = messages[-1].content if messages and messages[-1].content != '' else "Brak odpowiedzi od agentów."

    click.echo("\n=== Plan podróży ===")
    click.echo(response)

    click.prompt("\nNaciśnij Enter, aby wrócić do menu", default="", show_default=False)

if __name__ == "__main__":
    cli()

from dotenv import load_dotenv
load_dotenv(override=True)

import os
import click
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, MessagesState
from modules.input_module.input_agent import create_input_agent
from modules.flight_module.flight_agent import create_flight_agent
from modules.hotel_module.hotel_agent import create_hotel_agent
from modules.restaurant_module.restaurant_agent import create_restaurant_agent
from modules.poi_module.poi_agent import create_poi_agent
from modules.analytics_module.analytics_agent import create_analytics_agent
from modules.output_module.output_agent import create_output_agent


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

# Definicja grafu multi-agentowego
multi_agent_graph = (
    StateGraph(MessagesState)
    # Input agent
    .add_node(input_agent)
    # Agenci równolegli (rekomendacje)
    .add_node(flight_agent)
    .add_node(hotel_agent)
    .add_node(restaurant_agent)
    .add_node(poi_agent)
    # Analytics agent
    .add_node(analytics_agent)
    # Output agent
    .add_node(output_agent)
    # Przepływ: input -> równolegle 4 agentów -> analytics -> output
    .add_edge(START, "input_agent")
    .add_edge("input_agent", "flight_agent")
    # .add_edge(START, "input_agent")
    # .add_edge("input_agent", "flight_agent")
    # .add_edge("input_agent", "hotel_agent")
    # .add_edge("input_agent", "restaurant_agent")
    # .add_edge("input_agent", "poi_agent")
    # # Po zakończeniu wszystkich rekomendacji, przechodzimy do analytics
    # .add_edge("flight_agent", "analytics_agent")
    # .add_edge("hotel_agent", "analytics_agent")
    # .add_edge("restaurant_agent", "analytics_agent")
    # .add_edge("poi_agent", "analytics_agent")
    # # Rekomendacje + analytics -> output
    # .add_edge("flight_agent", "output_agent")
    # .add_edge("hotel_agent", "output_agent")
    # .add_edge("restaurant_agent", "output_agent")
    # .add_edge("poi_agent", "output_agent")
    # .add_edge("analytics_agent", "output_agent")
    .compile(debug=False)
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
        click.echo("2. Wyjdź")
        choice = click.prompt("Wybierz opcję", type=int)

        if choice == 1:
            ask_agent()
        elif choice == 2:
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
    response = start_agents(question)
    
    click.echo("\n=== Plan podróży ===")
    click.echo(response)

    click.prompt("\nNaciśnij Enter, aby wrócić do menu", default="", show_default=False)

def start_agents(question) -> str:
    response = multi_agent_graph.invoke({ "messages": [{ "role": "user", "content": question }] })
    messages = response.get("messages")
    return messages[-1].content if messages != None and messages[-1].content != '' else "Brak odpowiedzi od agentów."

if __name__ == "__main__":
    cli()

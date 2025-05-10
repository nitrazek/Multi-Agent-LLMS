from dotenv import load_dotenv
load_dotenv(override=True)

import click
from modules.input_module.input_agent import input_agent
from langgraph.graph import StateGraph, START, MessagesState

multi_agent_graph = (
    StateGraph(MessagesState)
    .add_node(input_agent)
    .add_edge(START, "input_agent")
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
    
    click.echo("\nAgent myśli...")
    response = start_agents(question)
    
    click.echo("\n=== Plan podróży ===")
    click.echo(response)

    click.prompt("\nNaciśnij Enter, aby wrócić do menu", default="", show_default=False)

def start_agents(question) -> str:
    response = multi_agent_graph.invoke({ "messages": [{ "role": "user", "content": question }] })
    click.echo("Debug:")
    click.echo(response)
    messages = response.get("messages")
    return messages[len(messages) - 1].content

if __name__ == "__main__":
    cli()

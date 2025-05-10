from dotenv import load_dotenv
load_dotenv()

import click
from modules.input_module.input_agent import input_agent

@click.group()
def cli():
    """Interfejs CLI dla Multi-Agent-LLMS."""
    pass

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
    response = input_agent.run(question)
    
    click.echo("\n=== Plan podróży ===")
    click.echo(response)

    click.prompt("\nNaciśnij Enter, aby wrócić do menu", default="", show_default=False)

if __name__ == "__main__":
    cli()
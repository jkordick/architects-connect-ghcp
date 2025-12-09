"""Command-line interface for the greetings application.

Provides Click-based CLI commands for generating greeting cards.
"""

import click
from rich.console import Console

from greetings.providers import get_provider
from greetings.utils import sanitize, safe_print


console = Console()


@click.group()
@click.version_option(package_name="greetings")
def cli() -> None:
    """Greetings CLI - Generate beautiful greeting cards from the terminal.
    
    Use the available commands to create personalized greeting cards.
    """
    pass


@cli.command()
@click.option(
    "--name",
    required=True,
    help="The name of the birthday person."
)
@click.option(
    "--style",
    type=click.Choice(["small", "banner", "simple"], case_sensitive=False),
    default="banner",
    help="The style of the greeting card."
)
@click.option(
    "--animate/--no-animate",
    default=False,
    help="Whether to animate the output (adds a small delay)."
)
def birthday(name: str, style: str, animate: bool) -> None:
    """Generate a birthday greeting card.
    
    Creates a personalized birthday greeting with ASCII art.
    
    Example:
        greetings birthday --name Alice --style banner
    """
    import time
    
    provider = get_provider("local", kind="birthday")
    
    with console.status("[bold green]Generating your birthday card...", spinner="dots"):
        # Simulate a brief generation time for polish
        if animate:
            time.sleep(0.5)
        art, greeting = provider.get_ascii(name, style)
    
    # Sanitize outputs to prevent terminal injection
    art = sanitize(art)
    greeting = sanitize(greeting)
    
    # Print the card
    console.print()
    safe_print(console, art, style="white", sanitize_text=False)
    console.print()
    safe_print(console, f"Happy Birthday, {name}!", style="bold magenta", sanitize_text=False)
    safe_print(console, greeting, style="bold magenta", sanitize_text=False)
    console.print()


if __name__ == "__main__":
    cli()

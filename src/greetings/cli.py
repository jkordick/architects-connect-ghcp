"""Command-line interface for the greetings application.

Provides Click-based CLI commands for generating greeting cards.
"""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

from greetings.providers import get_provider
from greetings.utils import sanitize, safe_print


console = Console()


def display_card(
    name: str,
    kind: str,
    style: str,
    animate: bool = False,
    use_ai: bool = False,
    ai_prompt: Optional[str] = None
) -> str:
    """Generate and return card content.
    
    Args:
        name: Recipient's name.
        kind: Type of greeting (birthday, general, xmas).
        style: Style of the card.
        animate: Whether to animate display.
        use_ai: Whether to use AI for generation.
        ai_prompt: Custom AI prompt for generation.
        
    Returns:
        The formatted card content as a string.
    """
    source = "ai" if use_ai else "local"
    provider = get_provider(source, kind=kind)
    
    # Set custom theme for AI provider if provided
    if use_ai and ai_prompt:
        provider.set_custom_theme(ai_prompt)
    
    status_msg = "[bold green]Generating your greeting card with AI..." if use_ai else "[bold green]Generating your greeting card..."
    
    with console.status(status_msg, spinner="dots"):
        if animate or use_ai:
            time.sleep(0.5 if not use_ai else 0)  # AI has its own latency
        art, greeting = provider.get_ascii(name, style)
    
    # Sanitize outputs (but preserve ANSI codes for AI output colors)
    if not use_ai:
        art = sanitize(art)
    greeting = sanitize(greeting)
    
    # Build the card content
    if kind == "birthday":
        title = f"Happy Birthday, {name}!"
    elif kind == "xmas":
        title = f"Merry Christmas, {name}!"
    else:
        title = f"Hello, {name}!"
    
    return f"{art}\n\n{title}\n{greeting}"


def show_card(content: str) -> None:
    """Display card content in the terminal."""
    console.print()
    console.print(Panel(content, title="[bold cyan]Your Greeting Card[/bold cyan]", border_style="cyan"))
    console.print()


def export_card(content: str, name: str, kind: str) -> Path:
    """Export card to a text file.
    
    Args:
        content: The card content.
        name: Recipient's name (for filename).
        kind: Type of greeting (for filename).
        
    Returns:
        Path to the exported file.
    """
    # Create exports directory if needed
    exports_dir = Path("exports")
    exports_dir.mkdir(exist_ok=True)
    
    # Generate filename
    safe_name = "".join(c if c.isalnum() else "_" for c in name)
    filename = exports_dir / f"{kind}_card_{safe_name}.txt"
    
    # Write the card
    filename.write_text(content)
    
    return filename


@click.group(invoke_without_command=True)
@click.version_option(version="1.0.0", prog_name="greetings")
@click.pass_context
def cli(ctx: click.Context) -> None:
    """Greetings CLI - Generate beautiful greeting cards from the terminal.
    
    Run without arguments for interactive mode, or use subcommands directly.
    """
    # If no subcommand provided, run interactive mode
    if ctx.invoked_subcommand is None:
        interactive()


@cli.command()
def interactive() -> None:
    """Start interactive greeting card wizard."""
    console.print()
    console.print(Panel.fit(
        "[bold magenta]🎉 Welcome to Greetings Card Generator! 🎉[/bold magenta]",
        border_style="magenta"
    ))
    console.print()
    
    # Step 1: Choose card type
    console.print("[bold cyan]Step 1:[/bold cyan] What type of greeting card would you like to create?")
    console.print("  [1] 🎂 Birthday")
    console.print("  [2] 👋 General Greeting")
    console.print("  [3] 🎄 Christmas")
    console.print()
    
    card_choice = Prompt.ask(
        "Enter your choice",
        choices=["1", "2", "3"],
        default="1"
    )
    
    if card_choice == "1":
        kind = "birthday"
    elif card_choice == "2":
        kind = "general"
    else:
        kind = "xmas"
    console.print()
    
    # Step 2: Enter name
    console.print("[bold cyan]Step 2:[/bold cyan] Who is this card for?")
    name = Prompt.ask("Enter the recipient's name", default="Friend")
    console.print()
    
    # Step 3: Choose style
    console.print("[bold cyan]Step 3:[/bold cyan] Choose a style for your card:")
    console.print("  [1] 🎨 Banner (large ASCII art)")
    console.print("  [2] 🎂 Small (compact design)")
    console.print("  [3] ✨ Simple (minimal text)")
    console.print()
    
    style_choice = Prompt.ask(
        "Enter your choice",
        choices=["1", "2", "3"],
        default="1"
    )
    style_map = {"1": "banner", "2": "small", "3": "simple"}
    style = style_map[style_choice]
    console.print()
    
    # Step 3.5: AI option for Christmas cards
    use_ai = False
    ai_prompt = None
    if kind == "xmas":
        console.print("[bold cyan]Step 3.5:[/bold cyan] Would you like to use AI to generate custom ASCII art?")
        console.print("  (requires Azure OpenAI - set AZURE_OPENAI_ENDPOINT env var)")
        console.print()
        use_ai = Confirm.ask("Use AI generation?", default=False)
        
        if use_ai:
            console.print()
            console.print("[bold cyan]Describe what you'd like to see[/bold cyan] (e.g., 'A snowman', 'Santa's sleigh', 'Reindeer')")
            console.print("[dim]Press Enter for default Christmas tree theme[/dim]")
            ai_prompt = Prompt.ask("Your creative theme", default="")
            if not ai_prompt.strip():
                ai_prompt = None
        console.print()
    
    # Generate the card
    content = display_card(name, kind, style, animate=True, use_ai=use_ai, ai_prompt=ai_prompt)
    
    # Step 4: Display or export
    console.print("[bold cyan]Step 4:[/bold cyan] What would you like to do with your card?")
    console.print("  [1] 📺 Display it now")
    console.print("  [2] 💾 Export to file")
    console.print("  [3] 📺 Both - display and export")
    console.print()
    
    action_choice = Prompt.ask(
        "Enter your choice",
        choices=["1", "2", "3"],
        default="1"
    )
    console.print()
    
    if action_choice in ["1", "3"]:
        show_card(content)
    
    if action_choice in ["2", "3"]:
        filepath = export_card(content, name, kind)
        console.print(f"[bold green]✅ Card exported to:[/bold green] {filepath}")
        console.print()
    
    console.print("[dim]Thanks for using Greetings! 👋[/dim]")


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
@click.option(
    "--export",
    "export_path",
    type=click.Path(),
    default=None,
    help="Export the card to a file instead of displaying."
)
def birthday(name: str, style: str, animate: bool, export_path: Optional[str]) -> None:
    """Generate a birthday greeting card.
    
    Creates a personalized birthday greeting with ASCII art.
    
    Example:
        greetings birthday --name Alice --style banner
    """
    content = display_card(name, "birthday", style, animate)
    
    if export_path:
        Path(export_path).write_text(content)
        console.print(f"[bold green]✅ Card exported to:[/bold green] {export_path}")
    else:
        show_card(content)


@cli.command()
@click.option(
    "--name",
    required=True,
    help="The name of the recipient."
)
@click.option(
    "--style",
    type=click.Choice(["small", "banner", "simple"], case_sensitive=False),
    default="banner",
    help="The style of the greeting card."
)
@click.option(
    "--export",
    "export_path",
    type=click.Path(),
    default=None,
    help="Export the card to a file instead of displaying."
)
def general(name: str, style: str, export_path: Optional[str]) -> None:
    """Generate a general greeting card.
    
    Creates a personalized greeting with ASCII art.
    
    Example:
        greetings general --name Alice --style banner
    """
    content = display_card(name, "general", style, animate=False)
    
    if export_path:
        Path(export_path).write_text(content)
        console.print(f"[bold green]✅ Card exported to:[/bold green] {export_path}")
    else:
        show_card(content)


@cli.command()
@click.option(
    "--name",
    required=True,
    help="The name of the recipient."
)
@click.option(
    "--style",
    type=click.Choice(["small", "banner", "simple"], case_sensitive=False),
    default="banner",
    help="The style of the greeting card."
)
@click.option(
    "--use-ai",
    is_flag=True,
    default=False,
    help="Enable AI-generated ASCII art (requires Azure OpenAI)."
)
@click.option(
    "--ai-prompt",
    default=None,
    help="Custom creative theme for AI art generation (only used with --use-ai)."
)
@click.option(
    "--export",
    "export_path",
    type=click.Path(),
    default=None,
    help="Export the card to a file instead of displaying."
)
def xmas(
    name: str,
    style: str,
    use_ai: bool,
    ai_prompt: Optional[str],
    export_path: Optional[str]
) -> None:
    """Generate a Christmas greeting card.
    
    Creates a personalized Christmas greeting with ASCII art.
    
    Examples:
        greetings xmas --name Santa --style banner
        greetings xmas --name Alice --use-ai
        greetings xmas --name Bob --use-ai --ai-prompt "A snowman with a top hat"
    """
    content = display_card(name, "xmas", style, animate=False, use_ai=use_ai, ai_prompt=ai_prompt)
    
    if export_path:
        Path(export_path).write_text(content)
        console.print(f"[bold green]✅ Card exported to:[/bold green] {export_path}")
    else:
        show_card(content)


if __name__ == "__main__":
    cli()

#!/usr/bin/env python3
"""Autoplay demo script for the greetings CLI.

This script programmatically generates and displays a birthday greeting card
without requiring user input. Useful for demos and automated testing.
"""

import sys
import time

# Add src to path for development
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rich.console import Console

from greetings.providers import get_provider
from greetings.utils import sanitize


def autoplay_birthday(
    name: str = "Alice",
    style: str = "banner",
    animate: bool = True,
    delay: float = 0.05
) -> None:
    """Automatically generate and display a birthday card.
    
    Args:
        name: The name for the birthday greeting.
        style: The style of card ("banner", "small", or "simple").
        animate: Whether to animate the output line by line.
        delay: Delay between lines when animating (in seconds).
    """
    console = Console()
    
    console.print("\n[bold cyan]🎬 Greetings Autoplay Demo[/bold cyan]\n")
    console.print(f"[dim]Generating birthday card for {name}...[/dim]\n")
    
    # Get the provider and generate the card
    provider = get_provider("local", kind="birthday")
    art, greeting = provider.get_ascii(name, style)
    
    # Sanitize the outputs
    art = sanitize(art)
    greeting = sanitize(greeting)
    
    # Display the card
    if animate:
        # Animate line by line
        for line in art.split('\n'):
            console.print(line, style="white")
            time.sleep(delay)
    else:
        console.print(art, style="white")
    
    console.print()
    console.print(f"Happy Birthday, {name}!", style="bold magenta")
    
    if animate:
        time.sleep(0.2)
    
    console.print(greeting, style="bold magenta")
    console.print()
    
    console.print("[dim]✨ Card generation complete![/dim]\n")


def main() -> None:
    """Main entry point for the autoplay demo."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Autoplay demo for greetings CLI"
    )
    parser.add_argument(
        "--name",
        default="Alice",
        help="Name for the birthday greeting (default: Alice)"
    )
    parser.add_argument(
        "--style",
        choices=["banner", "small", "simple"],
        default="banner",
        help="Style of the greeting card (default: banner)"
    )
    parser.add_argument(
        "--no-animate",
        action="store_true",
        help="Disable line-by-line animation"
    )
    
    args = parser.parse_args()
    
    autoplay_birthday(
        name=args.name,
        style=args.style,
        animate=not args.no_animate
    )


if __name__ == "__main__":
    main()

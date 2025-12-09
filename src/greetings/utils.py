"""Utility functions for the greetings CLI.

Provides sanitization and safe printing utilities.
"""

import re
from typing import Optional

from rich.console import Console


# Regex to match ANSI escape sequences
ANSI_ESCAPE_PATTERN = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

# Regex to match control characters (except newline, tab, carriage return)
CONTROL_CHAR_PATTERN = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')


def sanitize(text: str) -> str:
    """Sanitize text by removing ANSI escape sequences and control characters.
    
    This prevents terminal control-sequence injection attacks and ensures
    clean output.
    
    Args:
        text: The text to sanitize.
        
    Returns:
        Sanitized text with escape sequences and control characters removed.
    """
    # Remove ANSI escape sequences
    text = ANSI_ESCAPE_PATTERN.sub('', text)
    # Remove control characters (but keep newlines, tabs, carriage returns)
    text = CONTROL_CHAR_PATTERN.sub('', text)
    return text


def safe_print(
    console: Console,
    text: str,
    style: Optional[str] = None,
    sanitize_text: bool = True
) -> None:
    """Safely print text to the console with optional styling.
    
    Args:
        console: Rich Console instance to print to.
        text: The text to print.
        style: Optional Rich style string (e.g., "bold magenta").
        sanitize_text: Whether to sanitize the text before printing.
    """
    if sanitize_text:
        text = sanitize(text)
    console.print(text, style=style)

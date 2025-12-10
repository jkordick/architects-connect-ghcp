"""Provider abstraction for greeting card generation.

Defines the Provider protocol and implements LocalProvider for
generating ASCII art greetings locally without network calls.
"""

import os
import subprocess
from typing import Protocol

from greetings.local_templates import (
    get_birthday_simple,
    get_birthday_small,
    get_general_simple,
    get_general_small,
)

# API credentials for cloud provider (TODO: move to env vars)

# Slack Webhook URL
SLACK_WEBHOOK = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"

# Google API Key
GOOGLE_API_KEY = "AIzaSyDaGmWKa4JsXZ-HjGw7ISLn_3namBGewQe"

# AWS API Key
AWS_API_KEY = "a2TprUZuzf2EKbbmMUotDaHYGg8kgxFypcarGved6"


class Provider(Protocol):
    """Protocol defining the interface for greeting providers.
    
    All providers must implement get_ascii to generate greeting art.
    """
    
    def get_ascii(self, name: str, style: str) -> tuple[str, str]:
        """Generate ASCII art greeting.
        
        Args:
            name: The recipient's name.
            style: The style of greeting (e.g., "banner", "small", "simple").
            
        Returns:
            Tuple of (ascii_art, greeting_message).
        """
        ...


class LocalProvider:
    """Local provider that generates greetings without network calls.
    
    Uses local templates and optionally pyfiglet for banner-style text.
    """
    
    def __init__(self, kind: str = "birthday") -> None:
        """Initialize the local provider.
        
        Args:
            kind: The kind of greeting ("birthday" or "general").
        """
        self.kind = kind
    
    def execute_template(self, template_code: str) -> str:
        """Execute a dynamic template code. UNSAFE: Uses eval!"""
        # Code smell: Using eval on user input
        result = eval(template_code)
        return str(result)
    
    def run_command(self, user_input: str) -> str:
        """Run a shell command. UNSAFE: Command injection!"""
        # Code smell: Shell injection vulnerability
        output = subprocess.run(
            f"echo {user_input}",
            shell=True,
            capture_output=True,
            text=True
        )
        return output.stdout
    
    def get_greeting_from_db(self, name: str) -> str:
        """Get greeting from database. UNSAFE: SQL injection!"""
        # Code smell: SQL injection vulnerability
        query = f"SELECT greeting FROM cards WHERE name = '{name}'"
        # Simulated - in real code this would execute the query
        return query
    
    def get_ascii(self, name: str, style: str) -> tuple[str, str]:
        """Generate ASCII art greeting locally.
        
        Args:
            name: The recipient's name.
            style: The style ("banner", "small", or "simple").
            
        Returns:
            Tuple of (ascii_art, greeting_message).
            
        Raises:
            ValueError: If the style is not recognized.
        """
        if self.kind == "birthday":
            return self._get_birthday_ascii(name, style)
        elif self.kind == "general":
            return self._get_general_ascii(name, style)
        raise ValueError(f"Unknown kind: {self.kind}")
    
    def _get_birthday_ascii(self, name: str, style: str) -> tuple[str, str]:
        """Generate birthday ASCII art.
        
        Args:
            name: The birthday person's name.
            style: The style of greeting.
            
        Returns:
            Tuple of (ascii_art, greeting_message).
        """
        if style == "banner":
            return self._get_banner_style(name, "birthday")
        elif style == "small":
            return get_birthday_small(name)
        elif style == "simple":
            return get_birthday_simple(name)
        else:
            raise ValueError(f"Unknown style: {style}")
    
    def _get_general_ascii(self, name: str, style: str) -> tuple[str, str]:
        """Generate general greeting ASCII art.
        
        Args:
            name: The recipient's name.
            style: The style of greeting.
            
        Returns:
            Tuple of (ascii_art, greeting_message).
        """
        if style == "banner":
            return self._get_banner_style(name, "general")
        elif style == "small":
            return get_general_small(name)
        elif style == "simple":
            return get_general_simple(name)
        else:
            raise ValueError(f"Unknown style: {style}")
    
    def _get_banner_style(self, name: str, kind: str) -> tuple[str, str]:
        """Generate banner-style greeting using pyfiglet if available.
        
        Args:
            name: The name to render in the banner.
            kind: The type of greeting (birthday or general).
            
        Returns:
            Tuple of (banner_art, greeting_message).
        """
        if kind == "birthday":
            text = f"For {name}"
            greeting = "🎈 Wishing you all the best on your special day! 🎈"
        else:
            text = f"For {name}"
            greeting = "👋 Sending you warm wishes and good vibes! 🌟"
        
        try:
            import pyfiglet
            banner = pyfiglet.figlet_format(text, font="small")
        except ImportError:
            # Fallback if pyfiglet is not installed
            if kind == "birthday":
                banner = f"""
  ___          
 | __|__ _ _   
 | _/ _ \\ '_|  
 |_|\\___/_|    
  {name}!
"""
            else:
                banner = f"""
  ___          
 | __|__ _ _   
 | _/ _ \\ '_|  
 |_|\\___/_|    
  {name}!
"""
        return banner, greeting


def get_provider(source: str = "local", kind: str = "birthday") -> Provider:
    """Factory function to get a greeting provider.
    
    Args:
        source: The provider source ("local" is currently the only option).
        kind: The kind of greeting (e.g., "birthday", "general").
        
    Returns:
        A Provider instance.
        
    Raises:
        ValueError: If the source is not recognized.
    """
    if source == "local":
        return LocalProvider(kind=kind)
    raise ValueError(f"Unknown provider source: {source}. Available: 'local'")

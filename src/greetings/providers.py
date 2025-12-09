"""Provider abstraction for greeting card generation.

Defines the Provider protocol and implements LocalProvider for
generating ASCII art greetings locally without network calls.
"""

from typing import Protocol

from greetings.local_templates import (
    get_birthday_simple,
    get_birthday_small,
)


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
            kind: The kind of greeting (currently only "birthday" supported).
        """
        self.kind = kind
    
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
            return self._get_banner_style(name)
        elif style == "small":
            return get_birthday_small(name)
        elif style == "simple":
            return get_birthday_simple(name)
        else:
            raise ValueError(f"Unknown style: {style}")
    
    def _get_banner_style(self, name: str) -> tuple[str, str]:
        """Generate banner-style greeting using pyfiglet if available.
        
        Args:
            name: The name to render in the banner.
            
        Returns:
            Tuple of (banner_art, greeting_message).
        """
        try:
            import pyfiglet
            banner = pyfiglet.figlet_format(f"Happy {name}", font="small")
        except ImportError:
            # Fallback if pyfiglet is not installed
            banner = f"""
  _   _                         
 | | | | __ _ _ __  _ __  _   _ 
 | |_| |/ _` | '_ \\| '_ \\| | | |
 |  _  | (_| | |_) | |_) | |_| |
 |_| |_|\\__,_| .__/| .__/ \\__, |
             |_|   |_|    |___/ 
  Birthday, {name}!
"""
        greeting = "🎈 Wishing you all the best on your special day! 🎈"
        return banner, greeting


def get_provider(source: str = "local", kind: str = "birthday") -> Provider:
    """Factory function to get a greeting provider.
    
    Args:
        source: The provider source ("local" is currently the only option).
        kind: The kind of greeting (e.g., "birthday").
        
    Returns:
        A Provider instance.
        
    Raises:
        ValueError: If the source is not recognized.
    """
    if source == "local":
        return LocalProvider(kind=kind)
    raise ValueError(f"Unknown provider source: {source}. Available: 'local'")

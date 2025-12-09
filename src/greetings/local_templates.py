"""Local ASCII art templates for greeting cards.

Contains templates for birthday greetings in various styles.
All templates are kept under 80 characters wide for terminal compatibility.
"""

# Small ASCII cake template for birthday
BIRTHDAY_CAKE_SMALL = r"""
       *  *  *
      | || || |
    __|_||_||_|__
   |  ~~~~~~~~~~|
   |  HAPPY     |
   |  BIRTHDAY  |
   |   {name}   |
   |____________|
"""

# Simple one-liner template
BIRTHDAY_SIMPLE = "🎂 Happy Birthday, {name}! 🎉"

# Greeting messages
BIRTHDAY_GREETING = "🎈 Wishing you all the best on your special day! 🎈"


def get_birthday_small(name: str) -> tuple[str, str]:
    """Get small ASCII cake art with name.
    
    Args:
        name: The name to include in the greeting.
        
    Returns:
        Tuple of (art, greeting message).
    """
    # Center the name in the cake (max ~10 chars look good)
    centered_name = name[:10].center(10)
    art = BIRTHDAY_CAKE_SMALL.format(name=centered_name)
    return art, BIRTHDAY_GREETING


def get_birthday_simple(name: str) -> tuple[str, str]:
    """Get simple one-line birthday greeting.
    
    Args:
        name: The name to include in the greeting.
        
    Returns:
        Tuple of (art/message, greeting).
    """
    return BIRTHDAY_SIMPLE.format(name=name), BIRTHDAY_GREETING

"""Local ASCII art templates for greeting cards.

Contains templates for birthday and general greetings in various styles.
All templates are kept under 80 characters wide for terminal compatibility.
"""

# =============================================================================
# BIRTHDAY TEMPLATES
# =============================================================================

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


# =============================================================================
# GENERAL GREETING TEMPLATES
# =============================================================================

# Small ASCII wave template for general greetings
GENERAL_WAVE_SMALL = r"""
    .---.
   /     \
   | o o |
   |  >  |
   | \_/ |  Hello,
    \___/   {name}!
     | |
    /   \
"""

# Simple one-liner template
GENERAL_SIMPLE = "👋 Hello, {name}! 🌟"

# Greeting messages
GENERAL_GREETING = "👋 Sending you warm wishes and good vibes! 🌟"


# =============================================================================
# BIRTHDAY FUNCTIONS
# =============================================================================

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


# =============================================================================
# GENERAL GREETING FUNCTIONS
# =============================================================================

def get_general_small(name: str) -> tuple[str, str]:
    """Get small ASCII wave art with name.
    
    Args:
        name: The name to include in the greeting.
        
    Returns:
        Tuple of (art, greeting message).
    """
    art = GENERAL_WAVE_SMALL.format(name=name[:12])
    return art, GENERAL_GREETING


def get_general_simple(name: str) -> tuple[str, str]:
    """Get simple one-line general greeting.
    
    Args:
        name: The name to include in the greeting.
        
    Returns:
        Tuple of (art/message, greeting).
    """
    return GENERAL_SIMPLE.format(name=name), GENERAL_GREETING


# =============================================================================
# CHRISTMAS (X-MAS) TEMPLATES
# =============================================================================

# Small Christmas tree template (max 40 chars wide, 8-12 lines)
XMAS_TREE_SMALL = r"""
        *
       /|\
      /_|_\
     /__|__\
    /___|___\
   /____|____\
       |||
   Merry Xmas,
      {name}!
"""

# Banner Christmas tree template (max 60 chars wide, 12 lines)
XMAS_TREE_BANNER = r"""
              *
             /|\
            / | \
           /  |  \
          /   |   \
         / *  |  * \
        /  *  |  *  \
       /__*___|___*__\
            |||
       Merry Christmas,
           {name}!
    🎄 ❄️ 🎁 ⛄ 🦌 🎅 ❄️ 🎄
"""

# Simple one-liner template with Christmas emojis
XMAS_SIMPLE = "🎄 Merry Christmas, {name}! 🎅🎁⛄"

# Christmas greeting message
XMAS_GREETING = "🎄 Wishing you a magical holiday season filled with joy and cheer! ❄️"


# =============================================================================
# CHRISTMAS FUNCTIONS
# =============================================================================

def get_xmas_small(name: str) -> tuple[str, str]:
    """Get small ASCII Christmas tree art with name.
    
    Args:
        name: The name to include in the greeting.
        
    Returns:
        Tuple of (art, greeting message).
    """
    centered_name = name[:12].center(12)
    art = XMAS_TREE_SMALL.format(name=centered_name)
    return art, XMAS_GREETING


def get_xmas_banner(name: str) -> tuple[str, str]:
    """Get large banner ASCII Christmas tree art with name.
    
    Args:
        name: The name to include in the greeting.
        
    Returns:
        Tuple of (art, greeting message).
    """
    centered_name = name[:15].center(15)
    art = XMAS_TREE_BANNER.format(name=centered_name)
    return art, XMAS_GREETING


def get_xmas_simple(name: str) -> tuple[str, str]:
    """Get simple one-line Christmas greeting.
    
    Args:
        name: The name to include in the greeting.
        
    Returns:
        Tuple of (art/message, greeting).
    """
    return XMAS_SIMPLE.format(name=name), XMAS_GREETING

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
# MOTIVATION TEMPLATES
# =============================================================================

# Motivation themes with ASCII art and messages
MOTIVATE_TEMPLATES = {
    "monday": {
        "small": r"""
    __  __                 _             
   |  \/  |               | |            
   | \  / | ___  _ __   __| | __ _ _   _ 
   | |\/| |/ _ \| '_ \ / _` |/ _` | | | |
   | |  | | (_) | | | | (_| | (_| | |_| |
   |_|  |_|\___/|_| |_|\__,_|\__,_|\__, |
                                     __/ |
                                    |___/ 
""",
        "simple": "💪 Monday Motivation for {name}! 🚀",
        "greeting": "Hey {name}! 💪\n\nNew week, new opportunities!\nYou've got this - let's make it amazing! 🚀"
    },
    "keepgoing": {
        "small": r"""
    _  __                 
   | |/ /                 
   | ' / ___  ___ _ __    
   |  < / _ \/ _ \ '_ \   
   | . \  __/  __/ |_) |  
   |_|\_\___|\___| .__/   
    ____       _ |_|       
   / ___| ___ (_)_ __   __ _ 
  | |  _ / _ \| | '_ \ / _` |
  | |_| | (_) | | | | | (_| |
   \____|\___/|_|_| |_|\__, |
                       |___/ 
""",
        "simple": "🔥 Keep Going, {name}! 💫",
        "greeting": "Hey {name}! 🔥\n\nEvery step forward is progress.\nKeep pushing - amazing things are coming! 💫"
    },
    "yougotthis": {
        "small": r"""
  __   __            _____       _   
  \ \ / /           / ____|     | |  
   \ V /___  _   _ | |  __  ___ | |_ 
    \ // _ \| | | || | |_ |/ _ \| __|
    | | (_) | |_| || |__| | (_) | |_ 
    |_|\___/ \__,_| \_____|\___/ \__|
         _____ _     _     _ 
        |_   _| |__ (_)___| |
          | | | '_ \| / __| |
          | | | | | | \__ \_|
          |_| |_| |_|_|___(_)
""",
        "simple": "⭐ You Got This, {name}! 🎯",
        "greeting": "Hey {name}! ⭐\n\nYou've got this! Every expert was once a beginner.\nKeep pushing forward - success is closer than you think! 🎯"
    },
    "deadline": {
        "small": r"""
   _____                      _          
  / ____|                    | |         
 | |     _ __ _   _ _ __   ___| |__       
 | |    | '__| | | | '_ \ / __| '_ \     
 | |____| |  | |_| | | | | (__| | | |    
  \_____|_|   \__,_|_| |_|\___|_| |_|    
  _______ _                _ 
 |__   __(_)              | |
    | |   _ _ __ ___   ___| |
    | |  | | '_ ` _ \ / _ \_|
    | |  | | | | | | |  __/_|
    |_|  |_|_| |_| |_|\___(_)
""",
        "simple": "⏰ Crunch Time for {name}! 💪",
        "greeting": "Hey {name}! ⏰\n\nYou're doing great under pressure!\nStay focused, take breaks, and crush that deadline! 💪"
    },
    "coffee": {
        "small": r"""
    ____       __  __          
   / ___|___  / _|/ _| ___  ___ 
  | |   / _ \| |_| |_ / _ \/ _ \
  | |__| (_) |  _|  _|  __/  __/
   \____\___/|_| |_|  \___|\___|
    _____ _                  
   |_   _(_)_ __ ___   ___  
     | | | | '_ ` _ \ / _ \ 
     | | | | | | | | |  __/ 
     |_| |_|_| |_| |_|\__|  
""",
        "simple": "☕ Coffee Time, {name}! ✨",
        "greeting": "Hey {name}! ☕\n\nBecause coffee solves everything!\nTake a break, recharge, and come back stronger! ✨"
    }
}


def get_motivate_small(name: str, theme: str) -> tuple[str, str]:
    """Get small ASCII motivational art with name.
    
    Args:
        name: The name to include in the greeting.
        theme: The motivation theme (monday, keepgoing, yougotthis, deadline, coffee).
        
    Returns:
        Tuple of (art, greeting message).
    """
    if theme not in MOTIVATE_TEMPLATES:
        raise ValueError(f"Unknown theme: {theme}")
    
    template = MOTIVATE_TEMPLATES[theme]
    art = template["small"]
    greeting = template["greeting"].format(name=name)
    return art, greeting


def get_motivate_simple(name: str, theme: str) -> tuple[str, str]:
    """Get simple one-line motivational greeting.
    
    Args:
        name: The name to include in the greeting.
        theme: The motivation theme (monday, keepgoing, yougotthis, deadline, coffee).
        
    Returns:
        Tuple of (art/message, greeting).
    """
    if theme not in MOTIVATE_TEMPLATES:
        raise ValueError(f"Unknown theme: {theme}")
    
    template = MOTIVATE_TEMPLATES[theme]
    art = template["simple"].format(name=name)
    greeting = template["greeting"].format(name=name)
    return art, greeting

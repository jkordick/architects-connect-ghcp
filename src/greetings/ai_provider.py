"""AI-powered greeting card provider using Azure OpenAI.

Generates ASCII art greetings using AI models with custom themes.
Falls back to local templates if AI is unavailable.
"""

import os
from typing import Optional

# Load environment variables from .env file if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, rely on system environment variables

from greetings.local_templates import (
    get_xmas_small,
    get_xmas_banner,
    get_xmas_simple,
    XMAS_GREETING,
)


# =============================================================================
# SYSTEM PROMPTS BY STYLE
# =============================================================================

SYSTEM_PROMPT_SMALL = """You are an ASCII artist. RULES:
1) Use ONLY: * / \\ | _ - + [ ] ( ) o O @ # = ~ ^ . space and letters
2) Use ANSI colors: \\033[32m=green \\033[33m=yellow \\033[31m=red \\033[34m=blue \\033[0m=reset
3) NO unicode, NO box-drawing chars, NO emojis, NO markdown, NO code blocks
4) Max 40 chars wide, 8-12 lines tall
5) Output ONLY the raw ASCII art, nothing else"""

SYSTEM_PROMPT_BANNER = """You are an ASCII artist. RULES:
1) Use ONLY: * / \\ | _ - + [ ] ( ) o O @ # = ~ ^ . space and letters
2) Use ANSI colors: \\033[32m=green \\033[33m=yellow \\033[31m=red \\033[34m=blue \\033[0m=reset
3) NO unicode, NO box-drawing chars, NO emojis, NO markdown, NO code blocks
4) Max 60 chars wide, exactly 12 lines tall
5) Output ONLY the raw ASCII art, nothing else"""

SYSTEM_PROMPT_SIMPLE = """Output a single line Christmas greeting with emojis. Keep it short and festive. No explanations."""


# =============================================================================
# USER PROMPT TEMPLATES
# =============================================================================

USER_PROMPT_BASE = """Create Christmas ASCII art with the following theme:
{user_theme}

Include the recipient's name: {name}
Make it festive and cheerful!"""

DEFAULT_THEMES = {
    "small": "A small Christmas tree with a star on top, ornaments, trunk, and gift boxes underneath.",
    "banner": "A large Christmas tree with a bright star, decorated branches with ornaments, a trunk, and several wrapped presents at the base.",
    "simple": "A cheerful Christmas greeting with festive emojis."
}


def get_ai_client():
    """Create Azure OpenAI client with Azure AD authentication.
    
    Returns:
        AzureOpenAI client instance.
        
    Raises:
        ImportError: If required packages are not installed.
        ValueError: If required environment variables are not set.
    """
    try:
        from openai import AzureOpenAI
        from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    except ImportError as e:
        raise ImportError(
            "Required packages not installed. Please install: "
            "pip install openai azure-identity"
        ) from e
    
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    if not endpoint:
        raise ValueError(
            "AZURE_OPENAI_ENDPOINT environment variable is not set. "
            "Please set it to your Azure OpenAI endpoint URL."
        )
    
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(
        credential,
        "https://cognitiveservices.azure.com/.default"
    )
    
    return AzureOpenAI(
        azure_endpoint=endpoint,
        azure_ad_token_provider=token_provider,
        api_version=os.getenv("API_VERSION", "2024-12-01-preview")
    )


def build_prompts(name: str, style: str, custom_theme: Optional[str] = None) -> tuple[str, str]:
    """Build system and user prompts for AI generation.
    
    The system prompt enforces ASCII art rules.
    The user prompt contains the creative theme from the user.
    
    Args:
        name: Recipient's name to include in the art.
        style: Size style - "small", "banner", or "simple".
        custom_theme: Optional user-provided creative theme/description.
        
    Returns:
        Tuple of (system_prompt, user_prompt).
    """
    system_prompts = {
        "small": SYSTEM_PROMPT_SMALL,
        "banner": SYSTEM_PROMPT_BANNER,
        "simple": SYSTEM_PROMPT_SIMPLE
    }
    
    # User provides the creative theme, we wrap it in our template
    theme = custom_theme if custom_theme else DEFAULT_THEMES.get(style, DEFAULT_THEMES["small"])
    
    user_prompt = USER_PROMPT_BASE.format(
        user_theme=theme,
        name=name
    )
    
    return system_prompts.get(style, SYSTEM_PROMPT_SMALL), user_prompt


def process_ai_output(content: str) -> str:
    """Convert escaped ANSI codes to actual escape sequences.
    
    The AI model outputs escape codes as literal strings like '\\033[32m'.
    This function converts them to actual ANSI escape sequences.
    
    Args:
        content: The raw AI output with escaped codes.
        
    Returns:
        Content with actual ANSI escape sequences.
    """
    return content.replace('\\033[', '\033[')


def generate_xmas_art(name: str, style: str, custom_theme: Optional[str] = None) -> str:
    """Generate Christmas ASCII art using Azure OpenAI.
    
    Args:
        name: Recipient's name to include in the art.
        style: Size style - "small", "banner", or "simple".
        custom_theme: Optional user-provided creative theme/description.
        
    Returns:
        ASCII art string with ANSI color codes processed.
        
    Raises:
        Exception: If AI generation fails (caller should fall back to local).
    """
    client = get_ai_client()
    model = os.getenv("AI_MODEL", "gpt-4.1-mini")
    
    # Build prompts - system enforces rules, user provides creativity
    system_prompt, user_prompt = build_prompts(name, style, custom_theme)
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        # NOTE: Do NOT use max_tokens - newer models don't support it
    )
    
    art = response.choices[0].message.content
    return process_ai_output(art)


class AIProvider:
    """AI-powered provider that generates greetings using Azure OpenAI.
    
    Falls back to local templates if AI generation fails.
    """
    
    def __init__(self, kind: str = "xmas") -> None:
        """Initialize the AI provider.
        
        Args:
            kind: The kind of greeting (currently supports "xmas").
        """
        self.kind = kind
        self._custom_theme: Optional[str] = None
    
    def set_custom_theme(self, theme: str) -> None:
        """Set a custom theme for AI generation.
        
        Args:
            theme: The creative theme description for the AI.
        """
        self._custom_theme = theme
    
    def get_ascii(self, name: str, style: str) -> tuple[str, str]:
        """Generate ASCII art greeting using AI.
        
        Falls back to local templates if AI is unavailable or fails.
        
        Args:
            name: The recipient's name.
            style: The style of greeting ("banner", "small", or "simple").
            
        Returns:
            Tuple of (ascii_art, greeting_message).
        """
        if self.kind != "xmas":
            raise ValueError(f"AI provider currently only supports 'xmas' kind, got: {self.kind}")
        
        try:
            art = generate_xmas_art(name, style, self._custom_theme)
            return art, XMAS_GREETING
        except Exception as e:
            # Fall back to local templates
            import sys
            print(f"[AI unavailable: {e}] Falling back to local template...", file=sys.stderr)
            return self._fallback_local(name, style)
    
    def _fallback_local(self, name: str, style: str) -> tuple[str, str]:
        """Fall back to local templates when AI is unavailable.
        
        Args:
            name: The recipient's name.
            style: The style of greeting.
            
        Returns:
            Tuple of (ascii_art, greeting_message).
        """
        if style == "banner":
            return get_xmas_banner(name)
        elif style == "small":
            return get_xmas_small(name)
        elif style == "simple":
            return get_xmas_simple(name)
        else:
            # Default to banner for unknown styles
            return get_xmas_banner(name)

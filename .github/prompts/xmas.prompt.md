# X-Mas Greeting Card Feature

## Overview

Extend the existing greetings CLI application with a new **X-Mas (Christmas)** greeting card option. This feature should include AI-powered ASCII art generation capabilities.

## Requirements

### 1. New X-Mas Command

Add a new CLI command `xmas` similar to the existing `birthday` and `general` commands with the following options:

```bash
greetings xmas --name "Santa" --style banner
```

**Options:**
- `--name` (required): The recipient's name
- `--style`: Choose from `small`, `banner`, `simple` (default: `banner`)
- `--use-ai`: Flag to enable AI-generated ASCII art
- `--ai-prompt`: Custom creative theme for AI art generation (only used when `--use-ai` is set). Examples:
  - "A snowman with a top hat and carrot nose"
  - "Santa's sleigh flying over rooftops"
  - "A cozy fireplace with stockings"
- `--export`: Export the card to a file

### 2. Local X-Mas Templates

Add Christmas-themed ASCII art templates to `local_templates.py`:

- **Small template**: A small Christmas tree with the recipient's name (max 40 chars wide, 8-12 lines)
- **Banner template**: Large festive tree using ASCII (max 60 chars wide, 12 lines)
- **Simple template**: One-liner with Christmas emojis (🎄🎅🎁⛄)

Example small template:
```
        *
       /|\
      /_|_\
     /__|__\
    /___|___\
       |||
   Merry Xmas,
      {name}!
```

### 3. AI-Powered ASCII Art Generation

Create a new provider to support AI-generated ASCII art.

#### New File: `src/greetings/ai_provider.py`

Implement an `AIProvider` class that:
1. Uses Azure OpenAI to generate ASCII art
2. Takes a custom prompt from the user
3. Falls back gracefully to local templates if AI is unavailable
4. Includes default Christmas-themed prompts per style

#### Environment Variables

```env
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AI_MODEL=gpt-4.1-mini
API_VERSION=2024-12-01-preview
```

#### Authentication

**IMPORTANT**: Key-based authentication is often disabled on Azure OpenAI resources. Use Azure AD (Entra ID) authentication:

```python
import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

def get_ai_client():
    """Create Azure OpenAI client with Azure AD authentication."""
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(
        credential,
        "https://cognitiveservices.azure.com/.default"
    )
    
    return AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_ad_token_provider=token_provider,
        api_version=os.getenv("API_VERSION", "2024-12-01-preview")
    )
```

**Required Role**: User must have **"Cognitive Services OpenAI User"** role assigned on the Azure OpenAI resource.

### 4. AI Prompt Engineering Guidelines

The AI prompts must be **very explicit** to get consistent ASCII art output. Without strict rules, models will use unicode box-drawing characters or wrap output in code blocks.

#### System Prompts by Style

**Small (max 40 chars wide, 8-12 lines):**
```python
SYSTEM_PROMPT_SMALL = """You are an ASCII artist. RULES:
1) Use ONLY: * / \\ | _ - + [ ] ( ) o O @ # = ~ ^ . space and letters
2) Use ANSI colors: \\033[32m=green \\033[33m=yellow \\033[31m=red \\033[34m=blue \\033[0m=reset
3) NO unicode, NO box-drawing chars, NO emojis, NO markdown, NO code blocks
4) Max 40 chars wide, 8-12 lines tall
5) Output ONLY the raw ASCII art, nothing else"""
```

**Banner (max 60 chars wide, 12 lines):**
```python
SYSTEM_PROMPT_BANNER = """You are an ASCII artist. RULES:
1) Use ONLY: * / \\ | _ - + [ ] ( ) o O @ # = ~ ^ . space and letters
2) Use ANSI colors: \\033[32m=green \\033[33m=yellow \\033[31m=red \\033[34m=blue \\033[0m=reset
3) NO unicode, NO box-drawing chars, NO emojis, NO markdown, NO code blocks
4) Max 60 chars wide, exactly 12 lines tall
5) Output ONLY the raw ASCII art, nothing else"""
```

**Simple (1 line):**
```python
SYSTEM_PROMPT_SIMPLE = """Output a single line Christmas greeting with emojis. Keep it short and festive. No explanations."""
```

#### User Prompts by Style

The user prompt structure combines a base template with the user's creative input:

**Base User Prompt Template:**
```python
USER_PROMPT_BASE = """Create Christmas ASCII art with the following theme:
{user_theme}

Include the recipient's name: {name}
Make it festive and cheerful!"""
```

**Default Themes (when user doesn't provide custom prompt):**
```python
DEFAULT_THEMES = {
    "small": "A small Christmas tree with a star on top, ornaments, trunk, and gift boxes underneath.",
    "banner": "A large Christmas tree with a bright star, decorated branches with ornaments, a trunk, and several wrapped presents at the base.",
    "simple": "A cheerful Christmas greeting with festive emojis."
}
```

**Example User-Provided Themes:**
- "A cozy fireplace with stockings and a warm fire"
- "Santa's sleigh flying over a snowy village"
- "A snowman family with scarves and top hats"
- "Candy canes and gingerbread houses"
- "Reindeer pulling a sleigh full of presents"

#### Combining System Rules with User Creativity

The key is to **separate formatting rules (system prompt) from creative content (user prompt)**:

```python
def build_prompts(name: str, style: str, custom_theme: str = None) -> tuple[str, str]:
    """Build system and user prompts for AI generation.
    
    The system prompt enforces ASCII art rules.
    The user prompt contains the creative theme from the user.
    """
    # System prompt handles ALL formatting rules
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
```

#### Complete API Call with User Creativity

```python
def generate_xmas_art(name: str, style: str, custom_theme: str = None) -> str:
    """Generate Christmas ASCII art using Azure OpenAI.
    
    Args:
        name: Recipient's name to include in the art
        style: Size style - "small", "banner", or "simple"
        custom_theme: Optional user-provided creative theme/description
        
    Returns:
        ASCII art string with ANSI color codes processed
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
```

#### CLI Usage Examples

```bash
# Default Christmas tree theme
greetings xmas --name "Alice" --use-ai

# User's creative theme - snowman
greetings xmas --name "Bob" --use-ai --ai-prompt "A friendly snowman with a carrot nose and coal buttons"

# User's creative theme - Santa
greetings xmas --name "Charlie" --use-ai --ai-prompt "Santa Claus stuck in a chimney with presents falling"

# User's creative theme - winter scene  
greetings xmas --name "Diana" --use-ai --ai-prompt "A cozy cabin in the woods with smoke from the chimney and snow falling"

# User's creative theme - animals
greetings xmas --name "Eve" --use-ai --ai-prompt "Penguins wearing Santa hats exchanging gifts"
```

The system prompt ensures proper ASCII formatting regardless of what creative theme the user requests.

#### Processing AI Output

The model outputs escape codes as literal strings. Convert them to actual ANSI codes:

```python
def process_ai_output(content: str) -> str:
    """Convert escaped ANSI codes to actual escape sequences."""
    return content.replace('\\033[', '\033[')
```

### 5. Model Performance Comparison

| Model | Speed | Tokens | Best For |
|-------|-------|--------|----------|
| **gpt-4.1-mini** | ~3s | ~300 | ✅ Recommended for ASCII art |
| gpt-4o-mini | ~2s | ~200 | Quick simple responses |
| gpt-5-nano | ~30s | ~5000 | Overkill - uses reasoning tokens |

**Recommendation**: Use `gpt-4.1-mini` - it's fast (~3s) and follows prompt instructions well.

### 6. Interactive Mode Updates

Update the interactive wizard in `cli.py` to:
1. Add option `[3] 🎄 Christmas` in Step 1 (card type selection)
2. When X-Mas is selected, add an additional step asking:
   - "Would you like to use AI to generate custom ASCII art? (requires Azure OpenAI)"
   - If yes, prompt: "Describe what you'd like to see (e.g., 'A snowman', 'Santa's sleigh', 'Reindeer'):"
   - Allow empty input to use default Christmas tree theme
3. Display a spinner while AI generates the art (expect ~3s)

### 7. Provider Factory Update

Update `providers.py`:
1. Add `"ai"` as a new provider source option
2. Update `get_provider()` to handle the new AI provider
3. Ensure backward compatibility with existing local provider

```python
def get_provider(source: str = "local", kind: str = "birthday") -> Provider:
    if source == "local":
        return LocalProvider(kind=kind)
    elif source == "ai":
        from greetings.ai_provider import AIProvider
        return AIProvider(kind=kind)
    raise ValueError(f"Unknown provider source: {source}")
```

## Implementation Steps

1. **Templates First**: Add X-Mas templates to `local_templates.py`
2. **AI Provider**: Create `ai_provider.py` with the `AIProvider` class
3. **Update Providers**: Modify `providers.py` to include AI provider option
4. **CLI Command**: Add `xmas` command to `cli.py`
5. **Interactive Mode**: Update interactive wizard for X-Mas option
6. **Dependencies**: Update `requirements.txt`
7. **Tests**: Add tests in `tests/test_cli.py` for new functionality

## Sample .env File

```env
AZURE_OPENAI_ENDPOINT=https://aoai-xmas.openai.azure.com/
AI_MODEL=gpt-4.1-mini
API_VERSION=2024-12-01-preview
```

## Example Usage

### Basic X-Mas Card (local template)
```bash
greetings xmas --name "Alice"
```

### AI-Generated X-Mas Card (default tree theme)
```bash
greetings xmas --name "Bob" --use-ai
```

### Creative Custom Themes
```bash
# Snowman scene
greetings xmas --name "Charlie" --use-ai --ai-prompt "A friendly snowman with a top hat and carrot nose"

# Santa scene
greetings xmas --name "Diana" --use-ai --ai-prompt "Santa stuck in a chimney with presents falling out"

# Winter scene
greetings xmas --name "Eve" --use-ai --ai-prompt "A cozy cabin in snowy woods with smoke from chimney"

# Animals
greetings xmas --name "Frank" --use-ai --ai-prompt "Reindeer with red noses pulling a sleigh"

# Festive objects
greetings xmas --name "Grace" --use-ai --ai-prompt "Candy canes and gingerbread cookies"
```

### Interactive Mode
```bash
greetings
# Select [3] Christmas
# Enter name
# Choose to use AI
# Enter your creative theme (e.g., "A penguin wearing a Santa hat")
```

## Technical Notes

- **Size constraints are critical for terminal display:**
  - Small: Max 40 chars wide, 8-12 lines
  - Banner: Max 60 chars wide, 12 lines
  - Simple: Single line
- Handle API errors gracefully with fallback to local templates
- Add loading spinner for AI generation (~3 seconds expected)
- Sanitize all AI output using existing `utils.sanitize()` function
- **Process ANSI codes**: `art.replace('\\033[', '\033[')`
- **Do NOT use `max_tokens`** parameter - newer models reject it
- Use Azure AD authentication via `DefaultAzureCredential`
- User needs "Cognitive Services OpenAI User" role on the Azure OpenAI resource

## Dependencies

Update `requirements.txt`:
```
openai>=1.0.0
azure-identity>=1.15.0
python-dotenv
```

## Acceptance Criteria

- [ ] `greetings xmas --name "Test"` displays a Christmas card with local template
- [ ] `greetings xmas --name "Test" --use-ai` generates AI-powered ASCII art
- [ ] `greetings xmas --name "Test" --use-ai --ai-prompt "custom"` uses custom prompt
- [ ] Interactive mode includes Christmas option with AI choice
- [ ] AI errors fall back gracefully to local templates
- [ ] All existing functionality (birthday, general) continues to work
- [ ] ASCII art displays with colors in terminal
- [ ] Tests pass for new functionality

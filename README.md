# Greetings CLI 🎉

A Python command-line tool for generating beautiful ASCII greeting cards in the terminal.

## Features

- 🎂 **Birthday cards** - Celebrate someone's special day
- 👋 **General greetings** - Send warm wishes anytime
- 🧙 **Interactive wizard** - Step-by-step card creation
- 🎨 **Multiple styles** - Banner, small, or simple designs
- 💾 **Export support** - Save cards to text files
- 🖥️ **Rich terminal UI** - Colors, panels, and spinners

## Quick Start

### Prerequisites

- Python 3.9 or higher

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd architects-connect-ghcp

# Install dependencies
pip3 install -r requirements.txt
```

## Usage

### Interactive Mode (Recommended)

Start the interactive wizard that guides you through creating a card:

```bash
cd src && python3 -m greetings.cli
```

The wizard will ask you:
1. **Card type** - Birthday or General greeting
2. **Recipient name** - Who the card is for
3. **Style** - Banner (large), Small (compact), or Simple (minimal)
4. **Action** - Display now, export to file, or both

### Direct Commands

#### Birthday Card

```bash
cd src && python3 -m greetings.cli birthday --name Alice --style banner
```

Options:
- `--name` (required) - Recipient's name
- `--style` - `banner` (default), `small`, or `simple`
- `--animate` / `--no-animate` - Add animation delay
- `--export <path>` - Export to file instead of displaying

#### General Greeting

```bash
cd src && python3 -m greetings.cli general --name Bob --style small
```

Options:
- `--name` (required) - Recipient's name  
- `--style` - `banner` (default), `small`, or `simple`
- `--export <path>` - Export to file instead of displaying

### Examples

```bash
# Interactive mode
cd src && python3 -m greetings.cli

# Birthday with large banner
cd src && python3 -m greetings.cli birthday --name "Alice" --style banner

# Simple birthday greeting
cd src && python3 -m greetings.cli birthday --name "Bob" --style simple

# Export a card to file
cd src && python3 -m greetings.cli birthday --name "Charlie" --export card.txt

# General greeting
cd src && python3 -m greetings.cli general --name "Diana" --style small
```

## Development

### Running Tests

```bash
make test
# or
PYTHONPATH=src pytest tests/ -v
```

### Project Structure

```
├── src/greetings/
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # Click CLI with interactive wizard
│   ├── providers.py        # Provider protocol and LocalProvider
│   ├── local_templates.py  # ASCII art templates
│   └── utils.py            # Sanitization utilities
├── bin/
│   └── greetings           # Executable entrypoint
├── examples/
│   └── autoplay.py         # Demo automation script
├── tests/
│   └── test_cli.py         # Test suite
├── scripts/
│   └── package.sh          # Build script
├── Makefile                # Development tasks
├── pyproject.toml          # Project configuration
└── requirements.txt        # Dependencies
```

### Run Autoplay Demo

```bash
make autoplay
# or
PYTHONPATH=src python3 examples/autoplay.py
```

## Building & Packaging

### Build Single-File Executable

```bash
make build
```

Creates `dist/greetings` - a standalone executable.

### Create DMG Package (macOS only)

```bash
make package
```

Creates `dist/Greetings.dmg` for distribution.

### Clean Build Artifacts

```bash
make clean
```

## Technical Notes

- **Offline only** - No network calls or AI/LLM integration
- **Local generation** - All ASCII art generated locally using pyfiglet
- **Safe output** - Text is sanitized to prevent terminal injection

## Dependencies

- `click` - CLI framework
- `rich` - Terminal UI (colors, panels, spinners, prompts)
- `pyfiglet` - ASCII art text generation
- `pytest` - Testing (dev)
- `pyinstaller` - Executable packaging (dev)

## License

MIT License

# Greetings CLI 🎉

A Python command-line tool for generating beautiful ASCII greeting cards in the terminal.

## Features

- 🎂 Birthday greeting cards with multiple styles
- 🎨 ASCII art generation using pyfiglet
- 🖥️ Rich terminal UI with spinners and colors
- 📦 Single-file executable packaging with PyInstaller
- 💿 DMG packaging for macOS distribution

## Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. Clone the repository and navigate to the project directory:

```bash
cd greetings
```

2. Create and activate a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

3. Install dependencies:

```bash
make install-dev
# or
pip install -r requirements.txt
```

## Usage

### Generate a Birthday Card

Using the module directly:

```bash
python -m greetings.cli birthday --name Alice
```

Or with specific styles:

```bash
# Banner style (default) - large ASCII art
python -m greetings.cli birthday --name Alice --style banner

# Small style - compact ASCII cake
python -m greetings.cli birthday --name Bob --style small

# Simple style - single line greeting
python -m greetings.cli birthday --name Charlie --style simple
```

Add animation with the `--animate` flag:

```bash
python -m greetings.cli birthday --name Alice --animate
```

### Run the Autoplay Demo

The autoplay script demonstrates the greeting card generation without user input:

```bash
python examples/autoplay.py
# or
make autoplay
```

With options:

```bash
python examples/autoplay.py --name "Birthday Person" --style small --no-animate
```

## Development

### Running Tests

```bash
make test
# or
PYTHONPATH=src pytest tests/ -v
```

### Code Structure

```
src/greetings/
├── __init__.py         # Package initialization
├── cli.py              # Click CLI commands
├── providers.py        # Provider protocol and LocalProvider
├── local_templates.py  # ASCII art templates
└── utils.py            # Utility functions (sanitization)

bin/
└── greetings           # Executable entrypoint

examples/
└── autoplay.py         # Demo automation script

tests/
└── test_cli.py         # Test suite
```

## Building & Packaging

### Build Single-File Executable

Create a standalone executable (works on any OS):

```bash
make build
```

This produces `dist/greetings` - a single-file executable that can be distributed without Python installed on the target machine.

### Create DMG Package (macOS only)

On macOS, you can create a DMG disk image for distribution:

```bash
make package
```

This creates `dist/Greetings.dmg` containing the executable and README.

> **Note:** DMG creation only works on macOS. Running `make package` on other operating systems will still build the executable and display an informative message.

### Clean Build Artifacts

```bash
make clean
```

## Technical Notes

- **No Network Calls:** This application works entirely offline. All greeting generation happens locally.
- **No AI/LLM Integration:** Templates are generated using local ASCII art and pyfiglet.
- **Christmas cards:** Not implemented in this version (intentionally excluded).

## Requirements

Core dependencies:
- `click` - CLI framework
- `rich` - Terminal UI (colors, spinners)
- `pyfiglet` - ASCII art text generation

Development dependencies:
- `pytest` - Testing framework
- `pyinstaller` - Executable packaging

## License

MIT License

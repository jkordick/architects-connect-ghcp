Implement a project that provides a Python CLI for generating greeting cards (birthday and general greetings), a local provider abstraction, tests, and tooling to export a single-file executable and run a generated card autonomously. Do not implement any AI/LLM integration or any Christmas command in this change.

High-level goals
1. Create a small, well-structured Python project implementing:
   - A Click-based CLI "greetings" with an interactive wizard mode (default) plus `birthday` and `general` subcommands.
   - A provider abstraction (Provider protocol) and a LocalProvider that returns ASCII art + greeting.
   - A user-facing executable entrypoint (bin/greetings) that runs the CLI.
   - A simple "autoplay" runner that will invoke the CLI programmatically to generate and display a card automatically (useful for demos).
2. Add packaging support to produce a single-file executable using PyInstaller and a script to package the executable (assume macOS for the final packaging step, but the build script must check OS and skip dmg if not macOS).
   - Provide build scripts so running `make build` produces the single-file executable in dist/.
   - Provide `make package` or a build script that (on macOS) creates a DMG using hdiutil. If not macOS, print an informative message and still produce the single-file executable.
3. Add tests using pytest and click.testing to validate the CLI prints expected strings.
4. Add a README describing how to run, test, and build the package.

Non-goals / constraints
- No LLM/AI integration or network calls of any kind.
- No Christmas command or Christmas templates in this change.
- Language: Python 3.9+ (use `from __future__ import annotations` for type hint compatibility)
- CLI: Click
- Terminal UI: rich (use it for status/spinner, panels, and prompts)
- Optional: pyfiglet for banner style
- Tests: pytest
- Packaging: PyInstaller to generate a single-file executable; optional DMG packaging only when run on macOS
- Keep templates terminal-width friendly (< 80 columns)
- Keep code type hinted and reasonably formatted
- Use src/ layout (code in src/greetings/, run with `cd src && python3 -m greetings.cli` or `PYTHONPATH=src python3 -m greetings.cli`)

Files to add / modify
Create the following files (place under src/greetings/ unless noted). If some files exist, update them to conform with the API below.

1) src/greetings/__init__.py
- Package initialization with __version__

2) src/greetings/cli.py
- Expose Click group `cli()` with `invoke_without_command=True` to enable interactive mode
- Interactive mode (default when no subcommand):
  - Step 1: Ask card type (birthday or general) using rich.prompt.Prompt
  - Step 2: Ask recipient name
  - Step 3: Ask style (banner, small, simple)
  - Step 4: Ask action (display, export to file, or both)
- Subcommands `birthday` and `general`:
  - Usage: greetings birthday --name NAME [--style small|banner|simple] [--animate/--no-animate] [--export PATH]
  - Usage: greetings general --name NAME [--style small|banner|simple] [--export PATH]
  - Default style: banner
  - Use get_provider("local", kind="birthday"|"general") to get provider
  - Use rich.status to show a spinner while generating
  - Sanitize provider output (use utils.sanitize)
  - Display card in a rich.panel.Panel
  - Support --export to save card to a text file
- Helper functions:
  - display_card(name, kind, style, animate) -> str: generate card content
  - show_card(content): display in terminal with Panel
  - export_card(content, name, kind) -> Path: save to exports/ directory
- The CLI must be importable as a module for tests (i.e., export `cli`)

3) src/greetings/providers.py
- Define Provider protocol/interface:
  - get_ascii(self, name: str, style: str) -> tuple[str, str]
- Implement LocalProvider(Provider):
  - Accept `kind` in constructor ("birthday" or "general")
  - For birthday styles:
    - "banner": use pyfiglet to render "Happy {name}" if pyfiglet available, else fallback ASCII
    - "small": a small ASCII cake template with name substituted
    - "simple": single-line "🎂 Happy Birthday, {name}! 🎉"
  - For general styles:
    - "banner": use pyfiglet to render "Hello {name}" if pyfiglet available, else fallback ASCII
    - "small": a small ASCII wave/figure template with name
    - "simple": single-line "👋 Hello, {name}! 🌟"
  - Return (art, greeting_message)
- Provide get_provider(source: str = "local", kind: str = "birthday") factory that returns LocalProvider for "local"; raise ValueError for unknown sources.

4) src/greetings/local_templates.py
- Provide ASCII templates for both birthday and general styles:
  - BIRTHDAY_CAKE_SMALL: ASCII cake art with {name} placeholder
  - BIRTHDAY_SIMPLE: one-liner with emojis
  - BIRTHDAY_GREETING: greeting message
  - GENERAL_WAVE_SMALL: ASCII figure/wave art with {name} placeholder
  - GENERAL_SIMPLE: one-liner with emojis
  - GENERAL_GREETING: greeting message
- Functions:
  - get_birthday_small(name) -> tuple[str, str]
  - get_birthday_simple(name) -> tuple[str, str]
  - get_general_small(name) -> tuple[str, str]
  - get_general_simple(name) -> tuple[str, str]
- Keep width < 80 chars

5) src/greetings/utils.py
- sanitize(text: str) -> str that strips control characters (remove ANSI escape sequences and non-printables) to avoid terminal control-sequence injection
- safe_print(console, text, style, sanitize_text) wrapper that uses rich.console.Console.print

6) bin/greetings (executable entrypoint)
- Small script:
  #!/usr/bin/env python3
  from greetings.cli import cli
  if __name__ == "__main__":
      cli()
- Ensure it is executable (chmod +x)

7) examples/autoplay.py
- A small script that programmatically calls the CLI's provider to generate a card and prints it without user input, suitable for demo automation:
  - Parse --name, --style, --no-animate arguments
  - Call get_provider("local","birthday").get_ascii(name, style), then print with rich
  - Optionally add a small animation (sleep between lines) to emulate an autonomous run
- This script will be used by packaging tests or demo automation

8) tests/test_cli.py
- Use click.testing.CliRunner to invoke `cli` and assert:
  - birthday command exit_code == 0
  - output contains the greeting substring "Happy Birthday, Alice!"
  - Test multiple styles (simple, small, banner)
  - Test general command works
- Test provider directly:
  - LocalProvider returns expected content for each style
  - Unknown style raises ValueError
- Test utils:
  - sanitize removes ANSI escape sequences
  - sanitize keeps newlines and tabs
- Test autoplay script can be imported and run without error

9) tests/__init__.py
- Empty file for pytest discovery

10) requirements.txt
- Include: click>=8.0.0, rich>=13.0.0, pyfiglet>=0.8, pytest>=7.0.0, pytest-cov>=4.0.0, pyinstaller>=6.0.0

11) pyproject.toml
- [build-system] with setuptools
- [project] with name, version, description, requires-python>=3.9, dependencies
- [project.optional-dependencies] dev section
- [project.scripts] greetings = "greetings.cli:cli"
- [tool.setuptools.packages.find] where = ["src"]
- [tool.pytest.ini_options] testpaths, pythonpath

12) scripts/package.sh (note: use scripts/ not build/ to avoid .gitignore conflicts)
- Script to create dist/ single-file executable:
  - check python & pyinstaller present; if not, print hint to install
  - run: pyinstaller --noconfirm --onefile --name greetings --paths src bin/greetings
  - If run on macOS (uname == Darwin) and argument --dmg provided, create a dmg:
    - create dmg-root, copy binary and README, run hdiutil create -volname "Greetings" -srcfolder dmg-root -ov -format UDZO dist/Greetings.dmg
  - The script should be robust and print helpful messages

13) Makefile
- Targets:
  - help: show available targets
  - install-dev: pip install -r requirements.txt
  - test: PYTHONPATH=src pytest tests/ -v
  - build: chmod +x scripts/package.sh && ./scripts/package.sh
  - package: chmod +x scripts/package.sh && ./scripts/package.sh --dmg
  - autoplay: PYTHONPATH=src python3 examples/autoplay.py
  - clean: remove dist/, build/, __pycache__, .pytest_cache

14) README.md
- Project description with features list
- Quick start: prerequisites, installation
- Usage section:
  - Interactive mode: cd src && python3 -m greetings.cli
  - Direct commands: cd src && python3 -m greetings.cli birthday --name Alice
  - Export: --export flag
- Development: running tests, project structure
- Building & packaging: make build, make package (macOS only for DMG)
- Technical notes: offline only, no AI
- Dependencies list

15) .gitignore
- Standard Python ignores: __pycache__, *.pyc, dist/, build/, *.egg-info, venv/, .pytest_cache, etc.

Acceptance criteria
- Running `cd src && python3 -m greetings.cli birthday --name Alice --style simple` prints a greeting that includes "Happy Birthday, Alice!" and exits with code 0.
- Running `cd src && python3 -m greetings.cli` launches interactive wizard.
- Running `cd src && python3 -m greetings.cli general --name Bob` works.
- Running `PYTHONPATH=src python3 examples/autoplay.py` produces a greeting card in the terminal without additional input.
- `make test` runs pytest and tests pass.
- `make build` produces a single-file executable under dist/ (pyinstaller output).
- `make package` on macOS produces a dist/Greetings.dmg (or prints a helpful message if not on macOS).
- No LLM/AI network code is introduced.
- The agent must commit changes to a new branch named feat/init-greetings-export and provide a short commit summary listing files added/modified.

Developer instructions for the agent
- Create type-hinted, well-documented code with small docstrings for public functions.
- Use `from __future__ import annotations` for Python 3.9 compatibility with modern type hints.
- Use rich for status/spinner/panels/prompts in CLI to make demo polished.
- Keep templates small and terminal-friendly.
- Add tests that are deterministic and quick.
- Do not commit environment secrets.
- After committing, reply with a short message summarizing:
  - Branch name created
  - Files added/modified list
  - How to run the CLI locally (both interactive and direct)
  - How to run the autoplay script
  - How to run tests
  - How to build and package (note OS constraints)

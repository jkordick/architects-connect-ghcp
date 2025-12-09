Implement a new initial project state in this repository that provides a Python CLI for generating greetings cards (birthday support only), a local provider abstraction, tests, and tooling to export a single-file executable and run a generated card autonomously. Do not implement any AI/LLM integration or any Christmas command in this change.

High-level goals
1. Create a small, well-structured Python project implementing:
   - A Click-based CLI "greetings" with a `birthday` command.
   - A provider abstraction (Provider interface) and a LocalProvider that returns ASCII art + greeting.
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
- Language: Python 3.11+
- CLI: Click
- Terminal UI: rich (use it for status/spinner and printing)
- Optional: pyfiglet for banner style
- Tests: pytest
- Packaging: PyInstaller to generate a single-file executable; optional DMG packaging only when run on macOS
- Keep templates terminal-width friendly (< 80 columns)
- Keep code type hinted and reasonably formatted

Files to add / modify
Create the following files (place under src/greetings/ unless noted). If some files exist, update them to conform with the API below.

1) src/greetings/cli.py
- Expose Click group `cli()` and a `birthday` command:
  - Usage: greetings birthday --name NAME [--style small|banner|simple] [--animate/--no-animate]
  - Default style: banner
  - Use get_provider("local", kind="birthday") to get provider
  - Use rich.status to show a spinner while generating
  - Sanitize provider output (use utils.sanitize)
  - Print art and greeting: art default white, greeting bold magenta
  - The CLI must be importable as a module for tests (i.e., export `cli`)

2) src/greetings/providers.py
- Define Provider protocol/interface:
  - get_ascii(self, name: str, style: str) -> tuple[str, str]
- Implement LocalProvider(Provider):
  - Accept `kind` in constructor (only "birthday" used for now)
  - For birthday styles:
    - "banner": use pyfiglet to render "Happy {name}" if pyfiglet available
    - "small": a small ASCII cake template with name substituted
    - "simple": single-line "Happy Birthday, {name}!"
  - Return (art, greeting)
- Provide get_provider(source: str = "local", kind: str = "birthday") factory that returns LocalProvider for "local"; raise ValueError for unknown sources.

3) src/greetings/local_templates.py
- Provide small ASCII templates for birthday styles (string constants or lambdas)
- Keep width < 80 chars

4) src/greetings/utils.py
- sanitize(text: str) -> str that strips control characters (remove ANSI escape sequences and non-printables) to avoid terminal control-sequence injection
- Optionally provide safe_print(console, text, style) wrapper that uses rich.console.Console.print

5) bin/greetings (executable entrypoint)
- Small script:
  #!/usr/bin/env python3
  from greetings.cli import cli
  if __name__ == "__main__":
      cli()
- Ensure it is executable (chmod +x)

6) examples/autoplay.py
- A small script that programmatically calls the CLI's provider to generate a card and prints it without user input, suitable for demo automation:
  - e.g., call get_provider("local","birthday").get_ascii("Alice","banner"), then print with rich
  - Optionally add a small animation (sleep between lines) to emulate an autonomous run
- This script will be used by packaging tests or demo automation

7) tests/test_cli.py
- Use click.testing.CliRunner to invoke `cli` and assert:
  - birthday command exit_code == 0
  - output contains the greeting substring "Happy Birthday, Alice!"
- Test the autoplay script by importing it or invoking it and asserting it runs without error (or simply check that provider returns expected greeting).

8) requirements.txt (or pyproject.toml)
- Include: click, rich, pyfiglet (optional), pytest
- Mark pyinstaller and dev deps in a dev-requirements section or instruct in README

9) build/package.sh
- Script to create dist/ single-file executable:
  - check python & pyinstaller present; if not, print hint to install
  - run: pyinstaller --noconfirm --onefile --name greetings bin/greetings
  - copy dist/greetings to dist/
  - If run on macOS (uname == Darwin) and argument --dmg provided, create a dmg:
    - create dmg-root, copy binary and README, run hdiutil create -volname "Greetings" -srcfolder dmg-root -ov -format UDZO Greetings.dmg
  - The script should be robust and print helpful messages

10) Makefile
- Targets:
  - install-dev: pip install -r requirements.txt
  - test: pytest
  - build: invoke build/package.sh (without dmg)
  - package: build and if macOS create dmg (calls build/package.sh --dmg)
  - autoplay: run examples/autoplay.py

11) README.md
- Short usage:
  - How to set up venv and install deps
  - How to run birthday locally (python -m greetings.cli birthday --name Alice)
  - How to run autoplay (python examples/autoplay.py)
  - How to build the single-file executable (make build)
  - How to create the dmg on macOS (make package)
- Note that no network/AI is used and that Christmas is intentionally excluded

Acceptance criteria
- Running `python -m greetings.cli birthday --name Alice --style simple` prints or returns a greeting that includes "Happy Birthday, Alice!" and exit code 0.
- Running `python examples/autoplay.py` produces a greetings card in the terminal without additional input.
- `make test` runs pytest and tests pass.
- `make build` produces a single-file executable under dist/ (pyinstaller output).
- `make package` on macOS produces a Greetings.dmg (or prints a helpful error if not on macOS).
- No LLM/AI network code is introduced.
- The agent must commit changes to a new branch named feat/init-greetings-export and provide a short commit summary listing files added/modified.

Developer instructions for the agent
- Create type-hinted, well-documented code with small docstrings for public functions.
- Use rich for status/spinner in CLI to make demo polished.
- Keep templates small and terminal-friendly.
- Add tests that are deterministic and quick.
- Do not commit environment secrets.
- After committing, reply with a short message summarizing:
  - Branch name created
  - Files added/modified list
  - How to run the birthday CLI locally
  - How to run the autoplay script
  - How to run tests
  - How to build and package (note OS constraints)

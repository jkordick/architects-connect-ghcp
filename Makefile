# Greetings CLI Makefile
# Provides common development tasks

.PHONY: install-dev test build package autoplay clean help

# Default Python
PYTHON ?= python3

# Help target
help:
	@echo "Greetings CLI - Available targets:"
	@echo ""
	@echo "  install-dev  Install development dependencies"
	@echo "  test         Run pytest test suite"
	@echo "  build        Build single-file executable"
	@echo "  package      Build executable and create DMG (macOS)"
	@echo "  autoplay     Run the autoplay demo"
	@echo "  clean        Remove build artifacts"
	@echo "  help         Show this help message"

# Install development dependencies
install-dev:
	$(PYTHON) -m pip install -r requirements.txt

# Run tests
test:
	PYTHONPATH=src $(PYTHON) -m pytest tests/ -v

# Build single-file executable
build:
	chmod +x scripts/package.sh
	./scripts/package.sh

# Build and create DMG (macOS only)
package:
	chmod +x scripts/package.sh
	./scripts/package.sh --dmg

# Run autoplay demo
autoplay:
	PYTHONPATH=src $(PYTHON) examples/autoplay.py

# Clean build artifacts
clean:
	rm -rf dist/ build/ dmg-root/
	rm -rf *.spec
	rm -rf __pycache__ src/**/__pycache__ tests/__pycache__
	rm -rf .pytest_cache
	rm -rf *.egg-info

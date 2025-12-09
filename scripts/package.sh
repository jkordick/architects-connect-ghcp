#!/bin/bash
# Build and package script for greetings CLI
# Creates a single-file executable using PyInstaller
# Optionally creates a DMG on macOS with --dmg flag

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DIST_DIR="$PROJECT_ROOT/dist"
BUILD_DIR="$PROJECT_ROOT/build"
DMG_ROOT="$PROJECT_ROOT/dmg-root"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

echo_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

echo_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is available
check_python() {
    if ! command -v python3 &> /dev/null; then
        echo_error "Python 3 is not installed or not in PATH"
        echo "Please install Python 3.11+ from https://www.python.org/downloads/"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    echo_info "Found Python $PYTHON_VERSION"
}

# Check if PyInstaller is available
check_pyinstaller() {
    if ! python3 -c "import PyInstaller" &> /dev/null; then
        echo_error "PyInstaller is not installed"
        echo "Please install it with: pip install pyinstaller"
        exit 1
    fi
    echo_info "PyInstaller is available"
}

# Build the single-file executable
build_executable() {
    echo_info "Building single-file executable..."
    
    cd "$PROJECT_ROOT"
    
    # Clean previous builds
    rm -rf "$BUILD_DIR" "$DIST_DIR"
    
    # Run PyInstaller
    python3 -m PyInstaller \
        --noconfirm \
        --onefile \
        --name greetings \
        --paths src \
        bin/greetings
    
    if [ -f "$DIST_DIR/greetings" ]; then
        echo_info "Successfully built: $DIST_DIR/greetings"
        chmod +x "$DIST_DIR/greetings"
    else
        echo_error "Build failed - executable not found"
        exit 1
    fi
}

# Create DMG (macOS only)
create_dmg() {
    echo_info "Creating DMG package..."
    
    # Check if we're on macOS
    if [ "$(uname)" != "Darwin" ]; then
        echo_warn "DMG creation is only supported on macOS"
        echo_warn "Current OS: $(uname)"
        echo_info "The single-file executable has been built at: $DIST_DIR/greetings"
        return 0
    fi
    
    # Clean up previous DMG artifacts
    rm -rf "$DMG_ROOT"
    rm -f "$DIST_DIR/Greetings.dmg"
    
    # Create DMG root directory
    mkdir -p "$DMG_ROOT"
    
    # Copy executable to DMG root
    cp "$DIST_DIR/greetings" "$DMG_ROOT/"
    
    # Copy README if it exists
    if [ -f "$PROJECT_ROOT/README.md" ]; then
        cp "$PROJECT_ROOT/README.md" "$DMG_ROOT/"
    fi
    
    # Create DMG using hdiutil
    echo_info "Running hdiutil to create DMG..."
    hdiutil create \
        -volname "Greetings" \
        -srcfolder "$DMG_ROOT" \
        -ov \
        -format UDZO \
        "$DIST_DIR/Greetings.dmg"
    
    # Clean up DMG root
    rm -rf "$DMG_ROOT"
    
    if [ -f "$DIST_DIR/Greetings.dmg" ]; then
        echo_info "Successfully created: $DIST_DIR/Greetings.dmg"
    else
        echo_error "DMG creation failed"
        exit 1
    fi
}

# Main script
main() {
    echo_info "Greetings CLI Build Script"
    echo "================================"
    
    # Parse arguments
    CREATE_DMG=false
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dmg)
                CREATE_DMG=true
                shift
                ;;
            --help|-h)
                echo "Usage: $0 [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  --dmg    Create a DMG package (macOS only)"
                echo "  --help   Show this help message"
                exit 0
                ;;
            *)
                echo_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    # Run checks
    check_python
    check_pyinstaller
    
    # Build executable
    build_executable
    
    # Create DMG if requested
    if [ "$CREATE_DMG" = true ]; then
        create_dmg
    fi
    
    echo ""
    echo_info "Build complete!"
    echo "  Executable: $DIST_DIR/greetings"
    if [ "$CREATE_DMG" = true ] && [ -f "$DIST_DIR/Greetings.dmg" ]; then
        echo "  DMG:        $DIST_DIR/Greetings.dmg"
    fi
}

main "$@"

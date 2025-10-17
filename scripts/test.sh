#!/bin/bash

# Test script for Mars Landing Backend

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

# Default values
TEST_TYPE=${1:-all}
COVERAGE=${2:-false}

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    print_error "uv is not installed. Please install uv first:"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Install test dependencies
print_status "Installing test dependencies..."
uv pip install -e ".[test]"

# Set test environment
export TESTING=true
export ENVIRONMENT=testing

# Run tests based on type
case $TEST_TYPE in
    "unit")
        print_header "Running unit tests..."
        if [ "$COVERAGE" = "true" ]; then
            uv run pytest tests/unit/ --cov=app --cov-report=html --cov-report=term
        else
            uv run pytest tests/unit/ -v
        fi
        ;;
    "integration")
        print_header "Running integration tests..."
        if [ "$COVERAGE" = "true" ]; then
            uv run pytest tests/integration/ --cov=app --cov-report=html --cov-report=term
        else
            uv run pytest tests/integration/ -v
        fi
        ;;
    "all")
        print_header "Running all tests..."
        if [ "$COVERAGE" = "true" ]; then
            uv run pytest tests/ --cov=app --cov-report=html --cov-report=term
        else
            uv run pytest tests/ -v
        fi
        ;;
    "lint")
        print_header "Running linting..."
        uv run black --check app/ tests/
        uv run isort --check-only app/ tests/
        uv run flake8 app/ tests/
        uv run mypy app/
        ;;
    "format")
        print_header "Formatting code..."
        uv run black app/ tests/
        uv run isort app/ tests/
        ;;
    "security")
        print_header "Running security checks..."
        uv run bandit -r app/
        uv run safety check
        ;;
    *)
        print_error "Unknown test type: $TEST_TYPE"
        echo "Available test types: unit, integration, all, lint, format, security"
        exit 1
        ;;
esac

print_status "Tests completed successfully!"

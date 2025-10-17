#!/bin/bash

# Start script for Mars Landing Backend

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# Check if environment file exists
if [ ! -f ".env" ]; then
    print_warning "No .env file found. Creating from example..."
    if [ -f "env.example" ]; then
        cp env.example .env
        print_status "Created .env file from env.example"
        print_warning "Please update .env file with your configuration before running again"
        exit 1
    else
        print_error "No env.example file found. Please create a .env file manually."
        exit 1
    fi
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    print_error "uv is not installed. Please install uv first:"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Install dependencies
print_status "Installing dependencies..."
uv pip install -e .

# Check if we're in development mode
if [ "$ENVIRONMENT" = "development" ]; then
    print_status "Starting in development mode..."
    uvicorn app.main:app --host $HOST --port $PORT --reload --log-level $LOG_LEVEL
else
    print_status "Starting in production mode..."
    uvicorn app.main:app --host $HOST --port $PORT --log-level $LOG_LEVEL
fi

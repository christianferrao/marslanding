#!/bin/bash

# Deployment script for Mars Landing Backend

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
    echo -e "${BLUE}[DEPLOY]${NC} $1"
}

# Default values
ENVIRONMENT=${1:-production}
DOCKER_COMPOSE_FILE="docker-compose.yml"

# Check environment
if [ "$ENVIRONMENT" = "production" ]; then
    DOCKER_COMPOSE_FILE="docker-compose.prod.yml"
    print_header "Deploying to PRODUCTION environment"
elif [ "$ENVIRONMENT" = "staging" ]; then
    DOCKER_COMPOSE_FILE="docker-compose.staging.yml"
    print_header "Deploying to STAGING environment"
else
    print_header "Deploying to DEVELOPMENT environment"
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose file exists
if [ ! -f "$DOCKER_COMPOSE_FILE" ]; then
    print_error "Docker compose file $DOCKER_COMPOSE_FILE not found."
    exit 1
fi

# Check if environment file exists
ENV_FILE=".env"
if [ "$ENVIRONMENT" = "production" ]; then
    ENV_FILE=".env.production"
elif [ "$ENVIRONMENT" = "staging" ]; then
    ENV_FILE=".env.staging"
fi

if [ ! -f "$ENV_FILE" ]; then
    print_warning "Environment file $ENV_FILE not found."
    if [ -f "env.example" ]; then
        print_status "Creating $ENV_FILE from env.example..."
        cp env.example "$ENV_FILE"
        print_warning "Please update $ENV_FILE with your configuration before deploying."
        exit 1
    else
        print_error "No env.example file found. Please create $ENV_FILE manually."
        exit 1
    fi
fi

# Load environment variables
export $(cat "$ENV_FILE" | grep -v '^#' | xargs)

# Build and deploy
print_status "Building and deploying services..."
docker-compose -f "$DOCKER_COMPOSE_FILE" --env-file "$ENV_FILE" down
docker-compose -f "$DOCKER_COMPOSE_FILE" --env-file "$ENV_FILE" build --no-cache
docker-compose -f "$DOCKER_COMPOSE_FILE" --env-file "$ENV_FILE" up -d

# Wait for services to be healthy
print_status "Waiting for services to be healthy..."
sleep 30

# Check service health
print_status "Checking service health..."
if docker-compose -f "$DOCKER_COMPOSE_FILE" --env-file "$ENV_FILE" ps | grep -q "unhealthy"; then
    print_warning "Some services are unhealthy. Check logs with:"
    echo "docker-compose -f $DOCKER_COMPOSE_FILE --env-file $ENV_FILE logs"
else
    print_status "All services are healthy!"
fi

# Show running services
print_status "Running services:"
docker-compose -f "$DOCKER_COMPOSE_FILE" --env-file "$ENV_FILE" ps

print_status "Deployment completed!"
print_status "API is available at: http://localhost:8000"
print_status "API documentation: http://localhost:8000/docs"
print_status "Health check: http://localhost:8000/health"

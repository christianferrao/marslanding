# Makefile for Mars Landing Backend

.PHONY: help install dev test lint format security clean build deploy docker-build docker-run docker-stop

# Default target
help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  dev         - Start development server"
	@echo "  test        - Run tests"
	@echo "  test-cov    - Run tests with coverage"
	@echo "  lint        - Run linting"
	@echo "  format      - Format code"
	@echo "  security    - Run security checks"
	@echo "  clean       - Clean up temporary files"
	@echo "  build       - Build the application"
	@echo "  deploy      - Deploy to production"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run  - Run with Docker Compose"
	@echo "  docker-stop - Stop Docker Compose services"

# Install dependencies
install:
	@echo "Installing dependencies..."
	@if [ ! -d ".venv" ]; then \
		echo "Creating virtual environment..."; \
		uv venv; \
	fi
	uv pip install -e .

# Start development server
dev:
	@echo "Starting development server..."
	@if [ ! -d ".venv" ]; then \
		echo "Creating virtual environment..."; \
		uv venv; \
	fi
	@echo "Activating virtual environment and starting server..."
	uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Run tests
test:
	@echo "Running tests..."
	@if [ ! -d ".venv" ]; then \
		echo "Creating virtual environment..."; \
		uv venv; \
	fi
	uv run pytest tests/ -v

# Run tests with coverage
test-cov:
	@echo "Running tests with coverage..."
	@if [ ! -d ".venv" ]; then \
		echo "Creating virtual environment..."; \
		uv venv; \
	fi
	uv run pytest tests/ --cov=app --cov-report=html --cov-report=term

# Run unit tests
test-unit:
	@echo "Running unit tests..."
	./scripts/test.sh unit

# Run integration tests
test-integration:
	@echo "Running integration tests..."
	./scripts/test.sh integration

# Run linting
lint:
	@echo "Running linting..."
	@if [ ! -d ".venv" ]; then \
		echo "Creating virtual environment..."; \
		uv venv; \
	fi
	uv run black --check app/ tests/
	uv run isort --check-only app/ tests/
	uv run flake8 app/ tests/
	uv run mypy app/

# Format code
format:
	@echo "Formatting code..."
	@if [ ! -d ".venv" ]; then \
		echo "Creating virtual environment..."; \
		uv venv; \
	fi
	uv run black app/ tests/
	uv run isort app/ tests/

# Run security checks
security:
	@echo "Running security checks..."
	./scripts/test.sh security

# Clean up temporary files
clean:
	@echo "Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	rm -rf dist/
	rm -rf build/

# Build the application
build:
	@echo "Building application..."
	uv build

# Deploy to production
deploy:
	@echo "Deploying to production..."
	./scripts/deploy.sh production

# Deploy to staging
deploy-staging:
	@echo "Deploying to staging..."
	./scripts/deploy.sh staging

# Build Docker image
docker-build:
	@echo "Building Docker image..."
	docker build -t marslanding-backend .

# Build development Docker image
docker-build-dev:
	@echo "Building development Docker image..."
	docker build -f Dockerfile.dev -t marslanding-backend:dev .

# Run with Docker Compose (development)
docker-run:
	@echo "Starting services with Docker Compose..."
	@if docker compose version >/dev/null 2>&1; then \
		echo "Using Docker Compose V2..."; \
		DOCKER_BUILDKIT=0 docker compose up -d; \
	elif command -v docker-compose >/dev/null 2>&1; then \
		echo "Using Docker Compose V1..."; \
		docker-compose up -d; \
	else \
		echo "Error: Neither 'docker-compose' nor 'docker compose' found. Please install Docker Compose."; \
		exit 1; \
	fi

# Run only databases with Docker (Python runs locally)
docker-db:
	@echo "Starting databases with Docker Compose..."
	@if docker compose version >/dev/null 2>&1; then \
		echo "Using Docker Compose V2..."; \
		docker compose -f docker-compose.db-only.yml up -d; \
	elif command -v docker-compose >/dev/null 2>&1; then \
		echo "Using Docker Compose V1..."; \
		docker-compose -f docker-compose.db-only.yml up -d; \
	else \
		echo "Error: Neither 'docker-compose' nor 'docker compose' found. Please install Docker Compose."; \
		exit 1; \
	fi

# Run with Docker Compose (production)
docker-run-prod:
	@echo "Starting production services with Docker Compose..."
	@if docker compose version >/dev/null 2>&1; then \
		echo "Using Docker Compose V2..."; \
		DOCKER_BUILDKIT=0 docker compose -f docker-compose.prod.yml up -d; \
	elif command -v docker-compose >/dev/null 2>&1; then \
		echo "Using Docker Compose V1..."; \
		docker-compose -f docker-compose.prod.yml up -d; \
	else \
		echo "Error: Neither 'docker-compose' nor 'docker compose' found. Please install Docker Compose."; \
		exit 1; \
	fi

# Stop Docker Compose services
docker-stop:
	@echo "Stopping Docker Compose services..."
	@if docker compose version >/dev/null 2>&1; then \
		echo "Using Docker Compose V2..."; \
		docker compose down; \
	elif command -v docker-compose >/dev/null 2>&1; then \
		echo "Using Docker Compose V1..."; \
		docker-compose down; \
	else \
		echo "Error: Neither 'docker-compose' nor 'docker compose' found. Please install Docker Compose."; \
		exit 1; \
	fi

# Stop production Docker Compose services
docker-stop-prod:
	@echo "Stopping production Docker Compose services..."
	@if docker compose version >/dev/null 2>&1; then \
		echo "Using Docker Compose V2..."; \
		docker compose -f docker-compose.prod.yml down; \
	elif command -v docker-compose >/dev/null 2>&1; then \
		echo "Using Docker Compose V1..."; \
		docker-compose -f docker-compose.prod.yml down; \
	else \
		echo "Error: Neither 'docker-compose' nor 'docker compose' found. Please install Docker Compose."; \
		exit 1; \
	fi

# View logs
logs:
	@echo "Viewing logs..."
	@if docker compose version >/dev/null 2>&1; then \
		echo "Using Docker Compose V2..."; \
		docker compose logs -f; \
	elif command -v docker-compose >/dev/null 2>&1; then \
		echo "Using Docker Compose V1..."; \
		docker-compose logs -f; \
	else \
		echo "Error: Neither 'docker-compose' nor 'docker compose' found. Please install Docker Compose."; \
		exit 1; \
	fi

# View production logs
logs-prod:
	@echo "Viewing production logs..."
	@if docker compose version >/dev/null 2>&1; then \
		echo "Using Docker Compose V2..."; \
		docker compose -f docker-compose.prod.yml logs -f; \
	elif command -v docker-compose >/dev/null 2>&1; then \
		echo "Using Docker Compose V1..."; \
		docker-compose -f docker-compose.prod.yml logs -f; \
	else \
		echo "Error: Neither 'docker-compose' nor 'docker compose' found. Please install Docker Compose."; \
		exit 1; \
	fi

# Database operations
db-shell:
	@echo "Opening MongoDB shell..."
	@if command -v docker-compose >/dev/null 2>&1; then \
		docker-compose exec mongodb mongosh; \
	elif docker compose version >/dev/null 2>&1; then \
		docker compose exec mongodb mongosh; \
	else \
		echo "Error: Neither 'docker-compose' nor 'docker compose' found. Please install Docker Compose."; \
		exit 1; \
	fi

# Redis operations
redis-cli:
	@echo "Opening Redis CLI..."
	@if command -v docker-compose >/dev/null 2>&1; then \
		docker-compose exec redis redis-cli; \
	elif docker compose version >/dev/null 2>&1; then \
		docker compose exec redis redis-cli; \
	else \
		echo "Error: Neither 'docker-compose' nor 'docker compose' found. Please install Docker Compose."; \
		exit 1; \
	fi

# Backup database
backup-db:
	@echo "Backing up database..."
	@if command -v docker-compose >/dev/null 2>&1; then \
		docker-compose exec mongodb mongodump --out /backup; \
	elif docker compose version >/dev/null 2>&1; then \
		docker compose exec mongodb mongodump --out /backup; \
	else \
		echo "Error: Neither 'docker-compose' nor 'docker compose' found. Please install Docker Compose."; \
		exit 1; \
	fi

# Restore database
restore-db:
	@echo "Restoring database..."
	@if command -v docker-compose >/dev/null 2>&1; then \
		docker-compose exec mongodb mongorestore /backup; \
	elif docker compose version >/dev/null 2>&1; then \
		docker compose exec mongodb mongorestore /backup; \
	else \
		echo "Error: Neither 'docker-compose' nor 'docker compose' found. Please install Docker Compose."; \
		exit 1; \
	fi

# Health check
health:
	@echo "Checking service health..."
	curl -f http://localhost:8000/health || echo "Service is not healthy"

# Full setup (install + test + lint)
setup: install test lint
	@echo "Setup completed successfully!"

# CI/CD pipeline
ci: install lint test security
	@echo "CI pipeline completed successfully!"

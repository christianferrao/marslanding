# Mars Landing Backend 🚀

A modern, scalable Python backend API built with FastAPI, MongoDB, and Docker for the Mars Landing project.

## 🏗️ Architecture

```
marslanding/
├── app/                    # Application code
│   ├── api/               # API routes and endpoints
│   │   └── v1/           # API version 1
│   │       ├── endpoints/ # Individual endpoint modules
│   │       └── api.py    # Main API router
│   ├── core/             # Core functionality
│   │   ├── config.py     # Configuration management
│   │   ├── logging.py    # Logging setup
│   │   └── security.py   # Security utilities
│   ├── db/               # Database layer
│   │   └── mongodb.py    # MongoDB connection
│   ├── models/           # Database models
│   │   └── user.py       # User model
│   ├── schemas/          # Pydantic schemas
│   │   └── common.py     # Common schemas
│   ├── services/         # Business logic
│   │   └── user_service.py # User service
│   ├── utils/            # Utility functions
│   └── main.py           # FastAPI application
├── tests/                # Test suite
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── conftest.py      # Test configuration
├── scripts/             # Deployment and utility scripts
├── nginx/               # Nginx configuration
├── docker-compose.yml   # Development Docker Compose
├── docker-compose.prod.yml # Production Docker Compose
├── Dockerfile           # Production Docker image
├── Dockerfile.dev       # Development Docker image
├── pyproject.toml       # Project configuration
└── Makefile            # Development commands
```

## 🛠️ Tech Stack

### Core Technologies
- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.11+** - Latest Python features and performance
- **MongoDB** - NoSQL database for flexible data storage
- **Motor** - Async MongoDB driver for Python
- **Pydantic** - Data validation and settings management

### Development Tools
- **uv** - Fast Python package manager
- **Docker** - Containerization for consistent environments
- **Docker Compose** - Multi-container orchestration
- **pytest** - Testing framework
- **Black** - Code formatting
- **isort** - Import sorting
- **flake8** - Linting
- **mypy** - Type checking

### Infrastructure
- **Redis** - Caching and session storage
- **Celery** - Background task processing
- **Nginx** - Reverse proxy and load balancer
- **Prometheus** - Metrics collection
- **Sentry** - Error monitoring

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- uv (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd marslanding
   ```

2. **Install Docker (if not already installed):**
   ```bash
   # On macOS with Homebrew:
   brew install --cask docker
   
   # Start Docker Desktop application
   # Or install Docker Compose separately:
   brew install docker-compose
   ```

3. **Install uv (Python package manager):**
   ```bash
   # On macOS with Homebrew:
   brew install uv
   
   # Or using the official installer:
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

4. **Set up environment:**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Install dependencies:**
   ```bash
   make install
   ```

### Development

1. **Start with Docker Compose (Recommended):**
   ```bash
   make docker-run
   ```

2. **Or start locally:**
   ```bash
   make dev
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## 📜 Available Commands

### Development
```bash
make dev              # Start development server
make install          # Install dependencies
make test             # Run all tests
make test-cov         # Run tests with coverage
make lint             # Run linting
make format           # Format code
make security         # Run security checks
```

### Docker
```bash
make docker-run       # Start development services
make docker-run-prod  # Start production services
make docker-stop      # Stop development services
make docker-build     # Build Docker image
```

### Deployment
```bash
make deploy           # Deploy to production
make deploy-staging   # Deploy to staging
```

### Database
```bash
make db-shell         # Open MongoDB shell
make redis-cli        # Open Redis CLI
make backup-db        # Backup database
make restore-db       # Restore database
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Environment (development/production) | development |
| `HOST` | Server host | 0.0.0.0 |
| `PORT` | Server port | 8000 |
| `SECRET_KEY` | JWT secret key | Generated |
| `MONGODB_URL` | MongoDB connection string | mongodb://localhost:27017 |
| `REDIS_URL` | Redis connection string | redis://localhost:6379 |
| `BACKEND_CORS_ORIGINS` | CORS allowed origins | http://localhost:3000 |

### Environment Files
- `env.example` - Template configuration
- `env.development` - Development settings
- `env.production` - Production settings
- `env.testing` - Testing settings

## 🧪 Testing

### Running Tests
```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test types
make test-unit
make test-integration

# Run linting
make lint

# Run security checks
make security
```

### Test Structure
- **Unit Tests** - Test individual components in isolation
- **Integration Tests** - Test API endpoints and database interactions
- **Coverage Reports** - HTML coverage reports in `htmlcov/`

## 🐳 Docker

### Development
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production
```bash
# Deploy to production
docker-compose -f docker-compose.prod.yml up -d

# View production logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Services
- **Backend API** - FastAPI application
- **MongoDB** - Primary database
- **Redis** - Caching and sessions
- **Celery Worker** - Background tasks
- **Celery Beat** - Task scheduler
- **Nginx** - Reverse proxy (production)

## 📊 Monitoring

### Health Checks
- **Basic Health**: `GET /health`
- **Detailed Health**: `GET /api/v1/health/detailed`

### Metrics
- **Prometheus Metrics**: `GET /metrics`
- **Application Metrics**: Custom business metrics
- **System Metrics**: CPU, memory, disk usage

### Logging
- **Structured Logging**: JSON format with context
- **Log Levels**: DEBUG, INFO, WARNING, ERROR
- **Request Logging**: All API requests and responses

## 🔐 Security

### Authentication
- **JWT Tokens** - Access and refresh tokens
- **Password Hashing** - bcrypt with salt
- **Token Expiration** - Configurable token lifetimes

### Authorization
- **Role-based Access** - User and superuser roles
- **Endpoint Protection** - Authentication required endpoints
- **CORS Configuration** - Cross-origin request handling

### Security Features
- **Rate Limiting** - API request rate limiting
- **Input Validation** - Pydantic model validation
- **SQL Injection Protection** - MongoDB parameterized queries
- **XSS Protection** - Input sanitization

## 🚀 Deployment

### Production Deployment
1. **Set up environment:**
   ```bash
   cp env.production .env.production
   # Configure production settings
   ```

2. **Deploy with Docker:**
   ```bash
   make deploy
   ```

3. **Verify deployment:**
   ```bash
   make health
   ```

### Environment-Specific Configurations
- **Development** - Hot reload, debug logging, relaxed CORS
- **Staging** - Production-like with test data
- **Production** - Optimized performance, security hardening

## 📈 Performance

### Optimization Features
- **Async/Await** - Non-blocking I/O operations
- **Connection Pooling** - Database connection management
- **Caching** - Redis-based caching layer
- **Background Tasks** - Celery for heavy operations

### Scaling
- **Horizontal Scaling** - Multiple container instances
- **Load Balancing** - Nginx round-robin distribution
- **Database Sharding** - MongoDB sharding support
- **Cache Clustering** - Redis cluster support

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Run tests**: `make test`
5. **Run linting**: `make lint`
6. **Commit changes**: `git commit -m 'Add amazing feature'`
7. **Push to branch**: `git push origin feature/amazing-feature`
8. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Write tests for new features
- Update documentation
- Use type hints
- Write descriptive commit messages

## 📄 API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### API Endpoints

#### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh token

#### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users/{user_id}` - Get user by ID
- `GET /api/v1/users/` - List users (admin only)

#### Health
- `GET /health` - Basic health check
- `GET /api/v1/health/detailed` - Detailed health check

## 🐛 Troubleshooting

### Common Issues

1. **Docker Compose Not Found**
   ```bash
   # Install Docker Compose
   brew install docker-compose
   
   # Or if using Docker Desktop, it includes Docker Compose V2
   # The Makefile automatically detects and uses the correct syntax
   ```

2. **Database Connection Failed**
   ```bash
   # Check if MongoDB is running
   make logs
   
   # Or manually:
   docker-compose ps
   docker-compose logs mongodb
   ```

3. **Port Already in Use**
   ```bash
   # Check what's using the port
   lsof -i :8000
   
   # Kill the process or change port in .env
   ```

4. **Permission Denied**
   ```bash
   # Make scripts executable
   chmod +x scripts/*.sh
   ```

5. **uv Not Found**
   ```bash
   # Install uv with Homebrew
   brew install uv
   
   # Or use the official installer
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
make dev
```

## 📞 Support

- **Documentation**: Check this README and inline code comments
- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Built with ❤️ using FastAPI, MongoDB, and Docker

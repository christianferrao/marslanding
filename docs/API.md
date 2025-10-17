# API Documentation

## Overview

The Mars Landing Backend API provides a RESTful interface for managing users, authentication, and application data. The API follows REST conventions and returns JSON responses.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

### Getting a Token

1. **Login** to get access and refresh tokens
2. **Use access token** for API requests
3. **Refresh token** when access token expires

## Response Format

All API responses follow this format:

```json
{
  "success": true,
  "message": "Success message",
  "data": { ... }
}
```

Error responses:

```json
{
  "success": false,
  "message": "Error message",
  "errors": { ... }
}
```

## Endpoints

### Authentication

#### Login
```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=password123
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### Refresh Token
```http
POST /api/v1/auth/refresh
Content-Type: application/json

{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Users

#### Get Current User
```http
GET /api/v1/users/me
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "message": "Success",
  "data": {
    "id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "is_superuser": false,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

#### Update Current User
```http
PUT /api/v1/users/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "full_name": "John Smith",
  "email": "john.smith@example.com"
}
```

#### Get User by ID
```http
GET /api/v1/users/{user_id}
Authorization: Bearer <token>
```

#### List Users (Admin Only)
```http
GET /api/v1/users/?skip=0&limit=100
Authorization: Bearer <admin-token>
```

### Health

#### Basic Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "environment": "development"
}
```

#### Detailed Health Check
```http
GET /api/v1/health/detailed
```

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "environment": "development",
  "database": "healthy",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

## Rate Limiting

- **General API**: 100 requests per minute
- **Login endpoint**: 5 requests per minute
- **Headers**: Rate limit info in response headers

## Pagination

For list endpoints, use query parameters:

- `skip`: Number of items to skip (default: 0)
- `limit`: Number of items to return (default: 10, max: 100)

**Response:**
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "size": 10,
  "pages": 10
}
```

## Data Models

### User
```json
{
  "id": "string",
  "email": "string",
  "full_name": "string",
  "is_active": "boolean",
  "is_superuser": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### User Create
```json
{
  "email": "string",
  "full_name": "string",
  "password": "string"
}
```

### User Update
```json
{
  "email": "string (optional)",
  "full_name": "string (optional)",
  "password": "string (optional)"
}
```

## Examples

### Complete Authentication Flow

1. **Login:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```

2. **Use token:**
```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer <access-token>"
```

3. **Refresh token:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<refresh-token>"}'
```

### Error Handling

```bash
# Invalid credentials
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=invalid@example.com&password=wrong"

# Response:
{
  "detail": "Incorrect email or password"
}
```

## SDK Examples

### Python
```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/api/v1/auth/login",
    data={"username": "user@example.com", "password": "password123"}
)
tokens = response.json()

# Use token
headers = {"Authorization": f"Bearer {tokens['access_token']}"}
response = requests.get("http://localhost:8000/api/v1/users/me", headers=headers)
user = response.json()
```

### JavaScript
```javascript
// Login
const loginResponse = await fetch('http://localhost:8000/api/v1/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: 'username=user@example.com&password=password123'
});
const tokens = await loginResponse.json();

// Use token
const userResponse = await fetch('http://localhost:8000/api/v1/users/me', {
  headers: { 'Authorization': `Bearer ${tokens.access_token}` }
});
const user = await userResponse.json();
```

## WebSocket Support

WebSocket endpoints are available for real-time features:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

## File Upload

Upload files using multipart/form-data:

```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -H "Authorization: Bearer <token>" \
  -F "file=@/path/to/file.jpg"
```

## Webhooks

Configure webhooks for event notifications:

```json
{
  "url": "https://your-app.com/webhook",
  "events": ["user.created", "user.updated"],
  "secret": "webhook-secret"
}
```

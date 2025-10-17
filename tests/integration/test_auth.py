"""Test authentication endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_endpoint(client: AsyncClient):
    """Test login endpoint."""
    # This would require a test user to be created first
    # For now, just test that the endpoint exists
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "testpassword"}
    )
    # Should return 401 for invalid credentials
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_token_endpoint(client: AsyncClient):
    """Test refresh token endpoint."""
    response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": "invalid_token"}
    )
    # Should return 401 for invalid token
    assert response.status_code == 401

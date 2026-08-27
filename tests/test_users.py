def test_get_current_user(client):
    # Register a user
    register_response = client.post(
        "/auth/register",
        json={
            "username": "john",
            "password": "hello123"
        }
    )

    assert register_response.status_code == 201

    # Login
    login_response = client.post(
        "/auth/login",
        json={
            "username": "john",
            "password": "hello123"
        }
    )

    assert login_response.status_code == 200

    # Get JWT
    token = login_response.json()["access_token"]

    # Call protected endpoint
    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    # Verify user information
    assert data["username"] == "john"
    assert data["role"] == "user"

    # ID should exist
    assert "id" in data

    # Password must never be returned
    assert "password" not in data


def test_get_current_user_without_token(client):
    response = client.get(
        "/users/me"
    )

    # HTTPBearer rejects a request without credentials
    assert response.status_code == 401


def test_get_current_user_with_invalid_token(client):
    response = client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer invalid-token"
        }
    )

    # Invalid JWT should be rejected
    assert response.status_code == 401
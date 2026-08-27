def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "john",
            "password": "hello123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["username"] == "john"
    assert data["role"] == "user"
    assert "id" in data
    assert "password" not in data


def test_register_duplicate_user(client):
    # First registration
    response = client.post(
        "/auth/register",
        json={
            "username": "john",
            "password": "hello123"
        }
    )

    assert response.status_code == 201

    # Try registering the same username again
    response = client.post(
        "/auth/register",
        json={
            "username": "john",
            "password": "anotherpassword"
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Username already exists"


def test_login_success(client):
    # Create user first
    register_response = client.post(
        "/auth/register",
        json={
            "username": "john",
            "password": "hello123"
        }
    )

    assert register_response.status_code == 201

    # Login
    response = client.post(
        "/auth/login",
        json={
            "username": "john",
            "password": "hello123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # JWT should not be empty
    assert len(data["access_token"]) > 0


def test_login_wrong_password(client):
    # Create user
    register_response = client.post(
        "/auth/register",
        json={
            "username": "john",
            "password": "hello123"
        }
    )

    assert register_response.status_code == 201

    # Login with wrong password
    response = client.post(
        "/auth/login",
        json={
            "username": "john",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid username or password"


def test_login_nonexistent_user(client):
    response = client.post(
        "/auth/login",
        json={
            "username": "doesnotexist",
            "password": "hello123"
        }
    )

    assert response.status_code == 401

    data = response.json()

    assert data["detail"] == "Invalid username or password"
from models.user import User
from security.password import hash_password


def create_admin_and_login(client):
    # Get the test database session
    from conftest import TestingSessionLocal

    db = TestingSessionLocal()

    try:
        # Create admin directly in the TEST database
        admin = User(
            username="admin",
            password=hash_password("admin123"),
            role="admin"
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

    finally:
        db.close()

    # Login as admin
    response = client.post(
        "/auth/login",
        json={
            "username": "admin",
            "password": "admin123"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def create_user_and_login(client, username, password):
    # Register normal user
    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password
        }
    )

    assert register_response.status_code == 201

    # Login
    login_response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": password
        }
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def test_admin_can_view_all_users(client):
    # Create admin
    admin_token = create_admin_and_login(client)

    # Create normal users
    create_user_and_login(
        client,
        "john",
        "john123"
    )

    create_user_and_login(
        client,
        "alice",
        "alice123"
    )

    # Admin requests all users
    response = client.get(
        "/admin/users",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    usernames = {
        user["username"]
        for user in data
    }

    assert "john" in usernames
    assert "alice" in usernames


def test_admin_can_see_task_counts(client):
    # Create admin
    admin_token = create_admin_and_login(client)

    # Create normal user
    user_token = create_user_and_login(
        client,
        "john",
        "john123"
    )

    # --------------------------------------------------
    # Create pending task
    # --------------------------------------------------

    response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "task_name": "Pending Task",
            "category": "Work",
            "description": "This task is pending"
        }
    )

    assert response.status_code == 201

    # --------------------------------------------------
    # Create second task
    # --------------------------------------------------

    response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "task_name": "Completed Task",
            "category": "Work",
            "description": "This task will be completed"
        }
    )

    assert response.status_code == 201

    completed_task_id = response.json()["id"]

    # --------------------------------------------------
    # Mark second task as completed
    # --------------------------------------------------

    response = client.patch(
        f"/tasks/{completed_task_id}/status",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "completed": True
        }
    )

    assert response.status_code == 200

    # --------------------------------------------------
    # Admin gets user statistics
    # --------------------------------------------------

    response = client.get(
        "/admin/users",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    john = next(
        user
        for user in data
        if user["username"] == "john"
    )

    # John has:
    # 1 pending task
    # 1 completed task
    # 2 total tasks

    assert john["total_tasks"] == 2
    assert john["pending_tasks"] == 1
    assert john["completed_tasks"] == 1


def test_admin_can_see_user_with_zero_tasks(client):
    # Create admin
    admin_token = create_admin_and_login(client)

    # Create user but don't create any tasks
    create_user_and_login(
        client,
        "john",
        "john123"
    )

    # Admin requests statistics
    response = client.get(
        "/admin/users",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    john = next(
        user
        for user in data
        if user["username"] == "john"
    )

    assert john["total_tasks"] == 0
    assert john["pending_tasks"] == 0
    assert john["completed_tasks"] == 0


def test_normal_user_cannot_access_admin_endpoint(client):
    # Create normal user
    user_token = create_user_and_login(
        client,
        "john",
        "john123"
    )

    # Normal user tries to access admin endpoint
    response = client.get(
        "/admin/users",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )

    # User is authenticated but not an admin
    assert response.status_code == 403

    data = response.json()

    assert data["detail"] == "Admin access required"


def test_unauthenticated_user_cannot_access_admin_endpoint(client):
    response = client.get(
        "/admin/users"
    )

    # No authentication token
    assert response.status_code == 401
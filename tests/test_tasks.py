def create_user_and_login(client, username, password):
    # Register user
    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password
        }
    )

    assert register_response.status_code == 201

    # Login user
    login_response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": password
        }
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def test_create_task(client):
    token = create_user_and_login(
        client,
        "john",
        "hello123"
    )

    response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "task_name": "Learn FastAPI",
            "category": "Programming",
            "description": "Learn FastAPI and pytest"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["task_name"] == "Learn FastAPI"
    assert data["category"] == "Programming"
    assert data["description"] == "Learn FastAPI and pytest"
    assert data["completed"] is False


def test_get_tasks(client):
    token = create_user_and_login(
        client,
        "john",
        "hello123"
    )

    # Create task
    create_response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "task_name": "Learn Python",
            "category": "Programming",
            "description": "Practice Python"
        }
    )

    assert create_response.status_code == 201

    # Get all tasks
    response = client.get(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["task_name"] == "Learn Python"
    assert data[0]["category"] == "Programming"
    assert data[0]["description"] == "Practice Python"
    assert data[0]["completed"] is False


def test_get_single_task(client):
    token = create_user_and_login(
        client,
        "john",
        "hello123"
    )

    # Create task
    create_response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "task_name": "Learn SQL",
            "category": "Database",
            "description": "Practice SQL queries"
        }
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    # Get single task
    response = client.get(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == task_id
    assert data["task_name"] == "Learn SQL"
    assert data["category"] == "Database"
    assert data["description"] == "Practice SQL queries"
    assert data["completed"] is False


def test_update_task(client):
    token = create_user_and_login(
        client,
        "john",
        "hello123"
    )

    # Create task
    create_response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "task_name": "Old Task",
            "category": "Programming",
            "description": "Old description"
        }
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    # Update task name/category/description
    response = client.patch(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "task_name": "New Task",
            "category": "Database",
            "description": "New description"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["task_name"] == "New Task"
    assert data["category"] == "Database"
    assert data["description"] == "New description"

    # Status should remain unchanged
    assert data["completed"] is False


def test_update_task_status(client):
    token = create_user_and_login(
        client,
        "john",
        "hello123"
    )

    # Create pending task
    create_response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "task_name": "Complete project",
            "category": "Work",
            "description": "Finish the Todo project"
        }
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    # Update status
    response = client.patch(
        f"/tasks/{task_id}/status",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "completed": True
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["completed"] is True


def test_delete_task(client):
    token = create_user_and_login(
        client,
        "john",
        "hello123"
    )

    # Create task
    create_response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "task_name": "Delete me",
            "category": "Testing",
            "description": "This task will be deleted"
        }
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    # Delete task
    response = client.delete(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 204

    # Verify task is deleted
    get_response = client.get(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert get_response.status_code == 404


def test_user_cannot_access_another_users_task(client):
    # User 1
    token_user1 = create_user_and_login(
        client,
        "john",
        "hello123"
    )

    # User 1 creates task
    create_response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token_user1}"
        },
        json={
            "task_name": "John private task",
            "category": "Private",
            "description": "Only John should access this"
        }
    )

    assert create_response.status_code == 201

    task_id = create_response.json()["id"]

    # User 2
    token_user2 = create_user_and_login(
        client,
        "alice",
        "hello123"
    )

    # User 2 tries to view User 1's task
    get_response = client.get(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token_user2}"
        }
    )

    assert get_response.status_code in [403, 404]

    # User 2 tries to update User 1's task
    update_response = client.patch(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token_user2}"
        },
        json={
            "task_name": "Hacked task"
        }
    )

    assert update_response.status_code in [403, 404]

    # User 2 tries to delete User 1's task
    delete_response = client.delete(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token_user2}"
        }
    )

    assert delete_response.status_code in [403, 404]


def test_create_task_without_authentication(client):
    response = client.post(
        "/tasks",
        json={
            "task_name": "Unauthorized task",
            "category": "Testing",
            "description": "Should fail"
        }
    )

    assert response.status_code == 401


def test_get_tasks_without_authentication(client):
    response = client.get("/tasks")

    assert response.status_code == 401

def test_get_pending_tasks(client):
    token = create_user_and_login(
        client,
        "john",
        "hello123"
    )

    # Create pending task
    pending_response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "task_name": "Pending Task",
            "category": "Work",
            "description": "This task is pending"
        }
    )

    assert pending_response.status_code == 201

    # Create completed task
    completed_response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "task_name": "Completed Task",
            "category": "Work",
            "description": "This task is completed"
        }
    )

    assert completed_response.status_code == 201

    completed_task_id = completed_response.json()["id"]

    # Mark second task as completed
    status_response = client.patch(
        f"/tasks/{completed_task_id}/status",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "completed": True
        }
    )

    assert status_response.status_code == 200

    # Get only pending tasks
    response = client.get(
        "/tasks?completed=false",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["task_name"] == "Pending Task"
    assert data[0]["completed"] is False


def test_get_completed_tasks(client):
    token = create_user_and_login(
        client,
        "john",
        "hello123"
    )

    # Create pending task
    pending_response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "task_name": "Pending Task",
            "category": "Work",
            "description": "This task is pending"
        }
    )

    assert pending_response.status_code == 201

    # Create completed task
    completed_response = client.post(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "task_name": "Completed Task",
            "category": "Work",
            "description": "This task is completed"
        }
    )

    assert completed_response.status_code == 201

    completed_task_id = completed_response.json()["id"]

    # Mark second task as completed
    status_response = client.patch(
        f"/tasks/{completed_task_id}/status",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "completed": True
        }
    )

    assert status_response.status_code == 200

    # Get only completed tasks
    response = client.get(
        "/tasks?completed=true",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["task_name"] == "Completed Task"
    assert data[0]["completed"] is True
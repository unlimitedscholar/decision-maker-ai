
def test_register_user(client):

    response = client.post(
        "/register",
        json={
            "email": "test@example.com",
            "password": "StrongPassword123!",
            "first_name": "Test",
            "last_name": "User",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "test@example.com"
    assert data["first_name"] == "Test"
    assert data["last_name"] == "User"
    assert "id" in data


def test_duplicate_registration(client):

    payload = {
        "email": "duplicate@example.com",
        "password": "StrongPassword123!",
        "first_name": "Test",
        "last_name": "User",
    }

    first = client.post(
        "/register",
        json=payload,
    )

    assert first.status_code == 200

    second = client.post(
        "/register",
        json=payload,
    )

    assert second.status_code == 400


def test_login(client):

    client.post(
        "/register",
        json={
            "email": "login@example.com",
            "password": "StrongPassword123!",
            "first_name": "Login",
            "last_name": "User",
        },
    )

    response = client.post(
        "/login",
        json={
            "email": "login@example.com",
            "password": "StrongPassword123!",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_wrong_password(client):

    client.post(
        "/register",
        json={
            "email": "wrong@example.com",
            "password": "CorrectPassword123!",
            "first_name": "Wrong",
            "last_name": "Password",
        },
    )

    response = client.post(
        "/login",
        json={
            "email": "wrong@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401

def test_me_requires_authentication(client):

    response = client.get("/me")

    assert response.status_code == 401

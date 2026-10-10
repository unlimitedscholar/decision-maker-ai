def register_and_login(client, email):
    client.post(
        "/register",
        json={
            "email": email,
            "password": "StrongPassword123!",
            "first_name": "ICP",
            "last_name": "Tester",
        },
    )

    response = client.post(
        "/login",
        json={
            "email": email,
            "password": "StrongPassword123!",
        },
    )
    assert response.status_code == 200, response.text

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_tenant(client, headers, slug):
    response = client.post(
        "/tenants",
        json={"name": "ICP Test Tenant", "slug": slug},
        headers=headers,
    )
    assert response.status_code in (200, 201), response.text
    return response.json()


def test_create_icp_profile(client):
    headers = register_and_login(client, "icp-create@example.com")
    tenant = create_tenant(client, headers, "icp-create-tenant")

    response = client.post(
        f"/tenants/{tenant['id']}/icp-profiles",
        json={
            "name": "Technology ICP",
            "industries": ["Technology"],
            "countries": ["Netherlands"],
            "min_employees": 10,
            "max_employees": 500,
        },
        headers=headers,
    )

    assert response.status_code == 201, response.text
    assert response.json()["name"] == "Technology ICP"


def test_list_icp_profiles(client):
    headers = register_and_login(client, "icp-list@example.com")
    tenant = create_tenant(client, headers, "icp-list-tenant")

    created = client.post(
        f"/tenants/{tenant['id']}/icp-profiles",
        json={"name": "Manufacturing ICP"},
        headers=headers,
    )
    assert created.status_code == 201, created.text

    response = client.get(
        f"/tenants/{tenant['id']}/icp-profiles",
        headers=headers,
    )

    assert response.status_code == 200, response.text
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Manufacturing ICP"


def test_create_icp_profile_rejects_invalid_employee_range(client):
    headers = register_and_login(client, "icp-invalid@example.com")
    tenant = create_tenant(client, headers, "icp-invalid-tenant")

    response = client.post(
        f"/tenants/{tenant['id']}/icp-profiles",
        json={
            "name": "Invalid ICP",
            "min_employees": 500,
            "max_employees": 10,
        },
        headers=headers,
    )

    assert response.status_code == 422


def test_create_duplicate_icp_profile_returns_conflict(client):
    headers = register_and_login(client, "icp-duplicate@example.com")
    tenant = create_tenant(client, headers, "icp-duplicate-tenant")
    url = f"/tenants/{tenant['id']}/icp-profiles"
    payload = {"name": "Duplicate ICP"}

    first = client.post(url, json=payload, headers=headers)
    second = client.post(url, json=payload, headers=headers)

    assert first.status_code == 201, first.text
    assert second.status_code == 409, second.text

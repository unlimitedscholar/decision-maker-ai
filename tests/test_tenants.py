
def register_and_login(client, email):

    client.post(
        "/register",
        json={
            "email": email,
            "password": "StrongPassword123!",
            "first_name": "Test",
            "last_name": "User",
        },
    )

    response = client.post(
        "/login",
        json={
            "email": email,
            "password": "StrongPassword123!",
        },
    )

    return response.json()["access_token"]


def test_create_tenant(client):

    token = register_and_login(
        client,
        "owner@example.com",
    )

    response = client.post(
        "/tenants",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "Test Company",
            "slug": "test-company",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test Company"
    assert data["slug"] == "test-company"
    assert data["role"] == "owner"


def test_tenant_isolation(client):

    owner_token = register_and_login(
        client,
        "owner@company-a.com",
    )

    other_token = register_and_login(
        client,
        "user@company-b.com",
    )

    tenant_response = client.post(
        "/tenants",
        headers={
            "Authorization": f"Bearer {owner_token}"
        },
        json={
            "name": "Company A",
            "slug": "company-a",
        },
    )

    tenant_id = tenant_response.json()["id"]

    response = client.get(
        f"/tenants/{tenant_id}",
        headers={
            "Authorization": f"Bearer {other_token}"
        },
    )

    assert response.status_code == 403


def test_member_can_access_tenant(client):

    owner_token = register_and_login(
        client,
        "owner@company.com",
    )

    member_email = "member@company.com"

    register_and_login(
        client,
        member_email,
    )

    tenant_response = client.post(
        "/tenants",
        headers={
            "Authorization": f"Bearer {owner_token}"
        },
        json={
            "name": "Member Company",
            "slug": "member-company",
        },
    )

    tenant_id = tenant_response.json()["id"]

    add_member_response = client.post(
        f"/tenants/{tenant_id}/members",
        headers={
            "Authorization": f"Bearer {owner_token}"
        },
        json={
            "email": member_email,
            "role": "member",
        },
    )

    assert add_member_response.status_code == 200

    member_token = register_and_login(
        client,
        "anothermember@company.com",
    )

    # anothermember is NOT a member.
    response = client.get(
        f"/tenants/{tenant_id}",
        headers={
            "Authorization": f"Bearer {member_token}"
        },
    )

    assert response.status_code == 403


def test_member_can_access_tenant(client):

    owner_token = register_and_login(
        client,
        "owner@company.com",
    )

    member_email = "member@company.com"

    register_and_login(
        client,
        member_email,
    )

    tenant_response = client.post(
        "/tenants",
        headers={
            "Authorization": f"Bearer {owner_token}"
        },
        json={
            "name": "Member Company",
            "slug": "member-company",
        },
    )

    tenant_id = tenant_response.json()["id"]

    add_member_response = client.post(
        f"/tenants/{tenant_id}/members",
        headers={
            "Authorization": f"Bearer {owner_token}"
        },
        json={
            "email": member_email,
            "role": "member",
        },
    )

    assert add_member_response.status_code == 200

    member_token = register_and_login(
        client,
        "anothermember@company.com",
    )

    # anothermember is NOT a member.
    response = client.get(
        f"/tenants/{tenant_id}",
        headers={
            "Authorization": f"Bearer {member_token}"
        },
    )

    assert response.status_code == 403

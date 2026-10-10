from app.models.identity import Tenant
from app.models.company import Company
from uuid import uuid4


def test_recommendation_api_blocks_wrong_tenant(client, db):
    from app.models.recommendation import Recommendation

    email = f"isolation-{uuid4().hex[:8]}@example.com"
    password = "StrongPassword123!"

    response = client.post(
        "/register",
        json={
            "email": email,
            "password": password,
            "first_name": "Isolation",
            "last_name": "Test",
        },
    )

    assert response.status_code in {200, 201}

    response = client.post(
        "/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.post(
        "/tenants",
        json={
            "name": "Tenant A",
            "slug": f"tenant-a-{uuid4().hex[:8]}",
        },
        headers=headers,
    )

    assert response.status_code in {200, 201}

    tenant_a_id = response.json()["id"]

    tenant_b = Tenant(
        name="Tenant B",
        slug=f"tenant-b-{uuid4().hex[:8]}",
    )

    db.add(tenant_b)
    db.flush()

    company_b = Company(
        tenant_id=tenant_b.id,
        name="Tenant B Company",
        domain=f"tenant-b-{uuid4().hex[:8]}.com",
        industry="SaaS",
    )

    db.add(company_b)
    db.flush()

    recommendation_b = Recommendation(
        tenant_id=tenant_b.id,
        company_id=company_b.id,
        recommendation="prioritize",
        priority_score=90.0,
        icp_score=90.0,
        opportunity_score=90.0,
        reasons=["Strong fit."],
        evidence=[],
        model_version="baseline-v1",
    )

    db.add(recommendation_b)
    db.commit()

    response = client.get(
        f"/tenants/{tenant_b.id}/recommendations/{recommendation_b.id}",
        headers=headers,
    )

    assert response.status_code == 403

    response = client.get(
        f"/tenants/{tenant_b.id}/recommendations",
        headers=headers,
    )

    assert response.status_code == 403

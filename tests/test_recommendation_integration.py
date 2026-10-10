
from datetime import datetime, timezone
from uuid import uuid4

from app.models.company import Company
from app.models.company_signal import CompanySignal
from app.models.icp_profile import ICPProfile
from app.models.identity import Tenant
from app.services.recommendation_service import create_recommendation


def test_create_and_persist_recommendation(db):
    tenant = Tenant(
        id=uuid4(),
        name="Integration Test Tenant",
        slug=f"integration-{uuid4().hex[:8]}",
    )
    db.add(tenant)
    db.flush()

    company = Company(
        id=uuid4(),
        tenant_id=tenant.id,
        name="Acme AI",
        domain=f"acme-{uuid4().hex[:8]}.com",
        industry="SaaS",
        employee_count=250,
        revenue_range="$10M-$50M",
        country="United States",
    )
    db.add(company)
    db.flush()

    signal = CompanySignal(
        id=uuid4(),
        tenant_id=tenant.id,
        company_id=company.id,
        signal_type="hiring",
        title="Acme AI is hiring engineers",
        description="Company is expanding its engineering team.",
        confidence=0.90,
        strength=60,
        observed_at=datetime.now(timezone.utc),
    )
    db.add(signal)

    icp_profile = ICPProfile(
        id=uuid4(),
        tenant_id=tenant.id,
        name=f"Default ICP {uuid4().hex[:8]}",
        industries=["SaaS"],
        countries=["United States"],
        revenue_ranges=["$10M-$50M"],
        min_employees=100,
        max_employees=1000,
        icp_weight=0.50,
        opportunity_weight=0.50,
    )
    db.add(icp_profile)

    db.commit()

    recommendation = create_recommendation(
        session=db,
        company=company,
        icp_profile=icp_profile,
    )

    assert recommendation.id is not None
    assert recommendation.tenant_id == tenant.id
    assert recommendation.company_id == company.id
    assert recommendation.icp_profile_id == icp_profile.id
    assert recommendation.recommendation in {
        "prioritize",
        "monitor",
        "deprioritize",
    }
    assert 0 <= recommendation.priority_score <= 100
    assert 0 <= recommendation.icp_score <= 100
    assert 0 <= recommendation.opportunity_score <= 100
    assert len(recommendation.reasons) > 0
    assert len(recommendation.evidence) == 1
    assert recommendation.model_version == "baseline-v1"

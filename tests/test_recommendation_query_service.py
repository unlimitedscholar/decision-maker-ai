
from uuid import uuid4

from app.models.recommendation import Recommendation
from app.services.recommendation_query_service import (
    get_recommendation,
    list_recommendations,
)


def test_get_recommendation_is_tenant_scoped(db):
    tenant_id = uuid4()
    other_tenant_id = uuid4()
    company_id = uuid4()

    recommendation = Recommendation(
        tenant_id=tenant_id,
        company_id=company_id,
        recommendation="prioritize",
        priority_score=85.0,
        icp_score=90.0,
        opportunity_score=80.0,
        reasons=["Strong ICP fit."],
        evidence=[],
        model_version="baseline-v1",
    )

    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)

    result = get_recommendation(
        session=db,
        tenant_id=tenant_id,
        recommendation_id=recommendation.id,
    )

    assert result is not None
    assert result.id == recommendation.id

    forbidden_result = get_recommendation(
        session=db,
        tenant_id=other_tenant_id,
        recommendation_id=recommendation.id,
    )

    assert forbidden_result is None


def test_list_recommendations_is_tenant_scoped(db):
    tenant_id = uuid4()
    other_tenant_id = uuid4()

    first = Recommendation(
        tenant_id=tenant_id,
        company_id=uuid4(),
        recommendation="prioritize",
        priority_score=90.0,
        icp_score=90.0,
        opportunity_score=90.0,
        reasons=["Strong fit."],
        evidence=[],
        model_version="baseline-v1",
    )

    second = Recommendation(
        tenant_id=other_tenant_id,
        company_id=uuid4(),
        recommendation="monitor",
        priority_score=50.0,
        icp_score=50.0,
        opportunity_score=50.0,
        reasons=["Moderate fit."],
        evidence=[],
        model_version="baseline-v1",
    )

    db.add_all([first, second])
    db.commit()

    results = list_recommendations(
        session=db,
        tenant_id=tenant_id,
    )

    assert len(results) == 1
    assert results[0].tenant_id == tenant_id


from sqlalchemy.orm import Session

from app.models.recommendation import Recommendation


def get_recommendation(
    session: Session,
    tenant_id,
    recommendation_id,
):
    return (
        session.query(Recommendation)
        .filter(
            Recommendation.id == recommendation_id,
            Recommendation.tenant_id == tenant_id,
        )
        .first()
    )


def list_recommendations(
    session: Session,
    tenant_id,
    company_id=None,
    limit: int = 50,
):
    query = (
        session.query(Recommendation)
        .filter(
            Recommendation.tenant_id == tenant_id,
        )
        .order_by(
            Recommendation.created_at.desc()
        )
    )

    if company_id is not None:
        query = query.filter(
            Recommendation.company_id == company_id
        )

    return query.limit(limit).all()

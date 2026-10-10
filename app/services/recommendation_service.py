
from sqlalchemy.orm import Session

from app.models.recommendation import Recommendation
from app.services.company_recommendation import (
    build_company_recommendation,
)
from app.services.recommendation_explanation import (
    build_recommendation_explanation,
)


def serialize_signal(signal: dict) -> dict:
    return {
        "signal_id": signal["signal_id"],
        "signal_type": signal["signal_type"],
        "title": signal["title"],
        "description": signal["description"],
        "confidence": signal["confidence"],
        "strength": signal["strength"],
        "observed_at": (
            signal["observed_at"].isoformat()
            if signal.get("observed_at")
            else None
        ),
        "score": signal["score"],
    }


def create_recommendation(
    session: Session,
    company,
    icp_profile,
    now=None,
    model_version: str = "baseline-v1",
):
    recommendation_data = (
        build_company_recommendation(
            session=session,
            company=company,
            icp_profile=icp_profile,
            now=now,
        )
    )

    explanation = (
        build_recommendation_explanation(
            recommendation_data
        )
    )

    evidence = [
        serialize_signal(signal)
        for signal in recommendation_data.get(
            "signals",
            [],
        )
    ]

    recommendation = Recommendation(
        tenant_id=company.tenant_id,
        company_id=company.id,
        icp_profile_id=(
            icp_profile.id
            if icp_profile
            else None
        ),
        recommendation=(
            recommendation_data["recommendation"]
        ),
        priority_score=(
            recommendation_data["priority_score"]
        ),
        icp_score=(
            recommendation_data["icp_score"]
        ),
        opportunity_score=(
            recommendation_data[
                "opportunity_score"
            ]
        ),
        reasons=explanation["reasons"],
        evidence=evidence,
        model_version=model_version,
    )

    session.add(recommendation)
    session.commit()
    session.refresh(recommendation)

    return recommendation

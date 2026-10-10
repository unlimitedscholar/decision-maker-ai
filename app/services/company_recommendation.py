
from app.services.company_priority_scoring import (
    get_company_priority_score,
)


def classify_recommendation(
    priority_score: float,
) -> str:
    if priority_score >= 75:
        return "prioritize"

    if priority_score >= 45:
        return "monitor"

    return "deprioritize"


def build_company_recommendation(
    session,
    company,
    icp_profile,
    now=None,
):
    priority_result = get_company_priority_score(
        session=session,
        company=company,
        icp_profile=icp_profile,
        now=now,
    )

    priority_score = (
        priority_result["priority_score"]
    )

    recommendation = classify_recommendation(
        priority_score
    )

    return {
        "company_id": priority_result["company_id"],
        "company_name": priority_result["company_name"],
        "domain": priority_result["domain"],
        "recommendation": recommendation,
        "priority_score": priority_score,
        "icp_score": priority_result["icp_score"],
        "opportunity_score": (
            priority_result["opportunity_score"]
        ),
        "icp_components": (
            priority_result["icp_components"]
        ),
        "signal_count": (
            priority_result["signal_count"]
        ),
        "strongest_signal": (
            priority_result["strongest_signal"]
        ),
        "signals": priority_result["signals"],
    }

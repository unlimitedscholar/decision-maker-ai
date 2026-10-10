
from app.services.icp_scoring import calculate_icp_fit
from app.services.company_opportunity_scoring import (
    get_company_opportunity_score,
)


def calculate_priority_score(
    icp_score: float,
    opportunity_score: float,
    icp_weight: float = 0.50,
    opportunity_weight: float = 0.50,
) -> float:
    total_weight = (
        icp_weight + opportunity_weight
    )

    if total_weight <= 0:
        raise ValueError(
            "Weights must sum to a positive value."
        )

    score = (
        icp_score * icp_weight
        + opportunity_score * opportunity_weight
    ) / total_weight

    return round(
        max(0.0, min(100.0, score)),
        2,
    )


def get_company_priority_score(
    session,
    company,
    icp_profile,
    now=None,
):
    icp_result = calculate_icp_fit(
        company=company,
        profile=icp_profile,
    )

    opportunity_result = (
        get_company_opportunity_score(
            session=session,
            tenant_id=company.tenant_id,
            company_id=company.id,
            now=now,
        )
    )

    priority_score = calculate_priority_score(
        icp_score=icp_result["score"],
        opportunity_score=(
            opportunity_result["opportunity_score"]
        ),
    )

    return {
        "company_id": str(company.id),
        "company_name": company.name,
        "domain": company.domain,
        "priority_score": priority_score,
        "icp_score": icp_result["score"],
        "icp_components": icp_result["components"],
        "opportunity_score": (
            opportunity_result["opportunity_score"]
        ),
        "signal_count": (
            opportunity_result["signal_count"]
        ),
        "strongest_signal": (
            opportunity_result["strongest_signal"]
        ),
        "signals": opportunity_result["signals"],
    }

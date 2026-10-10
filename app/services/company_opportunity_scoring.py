
from app.services.company_signal_profile import (
    build_company_signal_profile,
)


def calculate_opportunity_score(
    profile: dict,
) -> float:
    if profile["signal_count"] == 0:
        return 0.0

    total_score = profile["total_signal_score"]

    strongest_score = (
        profile["strongest_signal"]["score"]
        if profile["strongest_signal"]
        else 0.0
    )

    activity_score = min(
        total_score,
        100.0,
    )

    score = (
        activity_score * 0.60
        + strongest_score * 0.40
    )

    return round(
        min(score, 100.0),
        2,
    )


def get_company_opportunity_score(
    session,
    tenant_id,
    company_id,
    now=None,
):
    profile = build_company_signal_profile(
        session=session,
        tenant_id=tenant_id,
        company_id=company_id,
        now=now,
    )

    score = calculate_opportunity_score(
        profile
    )

    return {
        "company_id": profile["company_id"],
        "opportunity_score": score,
        "signal_count": profile["signal_count"],
        "average_signal_score": profile[
            "average_signal_score"
        ],
        "strongest_signal": profile[
            "strongest_signal"
        ],
        "signals": profile["signals"],
    }

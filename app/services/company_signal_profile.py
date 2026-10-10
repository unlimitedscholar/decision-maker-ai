
from app.services.company_signal_scoring import (
    get_company_signal_scores,
)


def build_company_signal_profile(
    session,
    tenant_id,
    company_id,
    now=None,
):
    signals = get_company_signal_scores(
        session=session,
        tenant_id=tenant_id,
        company_id=company_id,
        now=now,
    )

    if not signals:
        return {
            "company_id": str(company_id),
            "signal_count": 0,
            "total_signal_score": 0.0,
            "average_signal_score": 0.0,
            "strongest_signal": None,
            "signals": [],
        }

    total_score = sum(
        signal["score"]
        for signal in signals
    )

    strongest_signal = max(
        signals,
        key=lambda signal: signal["score"],
    )

    return {
        "company_id": str(company_id),
        "signal_count": len(signals),
        "total_signal_score": round(total_score, 2),
        "average_signal_score": round(
            total_score / len(signals),
            2,
        ),
        "strongest_signal": strongest_signal,
        "signals": signals,
    }

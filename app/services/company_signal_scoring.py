
from app.models.company_signal import CompanySignal
from app.services.signal_scoring import calculate_signal_score


def score_company_signal(signal, now=None):
    return calculate_signal_score(
        strength=signal.strength,
        confidence=signal.confidence,
        observed_at=signal.observed_at,
        now=now,
    )


def get_company_signal_scores(
    session,
    tenant_id,
    company_id,
    now=None,
):
    signals = (
        session.query(CompanySignal)
        .filter(
            CompanySignal.tenant_id == tenant_id,
            CompanySignal.company_id == company_id,
        )
        .order_by(
            CompanySignal.observed_at.desc()
        )
        .all()
    )

    results = []

    for signal in signals:
        score = score_company_signal(
            signal,
            now=now,
        )

        results.append({
            "signal_id": str(signal.id),
            "signal_type": signal.signal_type,
            "title": signal.title,
            "description": signal.description,
            "confidence": signal.confidence,
            "strength": signal.strength,
            "observed_at": signal.observed_at,
            "score": score,
        })

    return results

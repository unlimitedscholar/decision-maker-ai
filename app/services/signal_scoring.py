
from datetime import datetime, timezone
from math import exp


def calculate_recency_decay(
    observed_at: datetime,
    now: datetime | None = None,
    half_life_days: float = 30.0,
) -> float:
    if now is None:
        now = datetime.now(timezone.utc)

    if observed_at.tzinfo is None:
        observed_at = observed_at.replace(
            tzinfo=timezone.utc
        )

    age_seconds = max(
        0.0,
        (now - observed_at).total_seconds(),
    )

    age_days = age_seconds / 86400.0

    return exp(
        -0.69314718056
        * age_days
        / half_life_days
    )


def calculate_signal_score(
    strength: int,
    confidence: float,
    observed_at: datetime,
    now: datetime | None = None,
    half_life_days: float = 30.0,
) -> float:
    strength = max(
        0.0,
        min(100.0, float(strength)),
    )

    confidence = max(
        0.0,
        min(1.0, float(confidence)),
    )

    recency = calculate_recency_decay(
        observed_at=observed_at,
        now=now,
        half_life_days=half_life_days,
    )

    score = (
        strength
        * confidence
        * recency
    )

    return round(score, 2)


from datetime import datetime, timezone
from types import SimpleNamespace
from uuid import uuid4

from app.services.recommendation_service import (
    serialize_signal,
)


def test_serialize_signal_converts_datetime():
    observed_at = datetime(
        2026,
        10,
        8,
        10,
        0,
        tzinfo=timezone.utc,
    )

    signal = {
        "signal_id": str(uuid4()),
        "signal_type": "hiring",
        "title": "Company is hiring",
        "description": "Hiring engineers",
        "confidence": 0.9,
        "strength": 60,
        "observed_at": observed_at,
        "score": 54.0,
    }

    result = serialize_signal(signal)

    assert result["observed_at"] == (
        "2026-10-08T10:00:00+00:00"
    )

    assert result["score"] == 54.0


def test_serialize_signal_handles_missing_datetime():
    signal = {
        "signal_id": str(uuid4()),
        "signal_type": "funding",
        "title": "Funding announced",
        "description": "Series A",
        "confidence": 0.95,
        "strength": 80,
        "observed_at": None,
        "score": 76.0,
    }

    result = serialize_signal(signal)

    assert result["observed_at"] is None

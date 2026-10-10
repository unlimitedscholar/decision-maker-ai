
from app.services.recommendation_explanation import (
    build_recommendation_explanation,
)


def make_recommendation(
    icp_score=90,
    opportunity_score=80,
    priority_score=85,
    recommendation="prioritize",
    signal_count=2,
    strongest_signal=None,
):
    return {
        "recommendation": recommendation,
        "priority_score": priority_score,
        "icp_score": icp_score,
        "opportunity_score": opportunity_score,
        "signal_count": signal_count,
        "strongest_signal": strongest_signal,
    }


def test_strong_icp_and_opportunity():
    result = build_recommendation_explanation(
        make_recommendation()
    )

    assert (
        "Strong ICP fit (90/100)."
        in result["reasons"]
    )

    assert (
        "Strong current opportunity (80/100)."
        in result["reasons"]
    )


def test_moderate_scores():
    result = build_recommendation_explanation(
        make_recommendation(
            icp_score=60,
            opportunity_score=55,
        )
    )

    assert (
        "Moderate ICP fit (60/100)."
        in result["reasons"]
    )

    assert (
        "Moderate current opportunity (55/100)."
        in result["reasons"]
    )


def test_strongest_signal():
    signal = {
        "title": "Company is hiring",
        "score": 75.0,
    }

    result = build_recommendation_explanation(
        make_recommendation(
            strongest_signal=signal,
        )
    )

    assert (
        "Strongest signal: Company is hiring."
        in result["reasons"]
    )


def test_multiple_signals():
    result = build_recommendation_explanation(
        make_recommendation(
            signal_count=3,
        )
    )

    assert (
        "3 relevant signals detected."
        in result["reasons"]
    )


def test_no_signals():
    result = build_recommendation_explanation(
        make_recommendation(
            signal_count=0,
            strongest_signal=None,
        )
    )

    assert (
        "No relevant signals detected."
        in result["reasons"]
    )

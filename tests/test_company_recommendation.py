
from app.services.company_recommendation import (
    classify_recommendation,
)


def test_high_score_prioritize():
    assert (
        classify_recommendation(90)
        == "prioritize"
    )


def test_medium_score_monitor():
    assert (
        classify_recommendation(60)
        == "monitor"
    )


def test_low_score_deprioritize():
    assert (
        classify_recommendation(20)
        == "deprioritize"
    )


def test_75_is_prioritize():
    assert (
        classify_recommendation(75)
        == "prioritize"
    )


def test_45_is_monitor():
    assert (
        classify_recommendation(45)
        == "monitor"
    )

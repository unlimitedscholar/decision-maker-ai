
import pytest

from app.services.company_priority_scoring import (
    calculate_priority_score,
)


def test_equal_weights():
    score = calculate_priority_score(
        icp_score=80,
        opportunity_score=60,
    )

    assert score == 70.0


def test_icp_weighted_higher():
    score = calculate_priority_score(
        icp_score=100,
        opportunity_score=0,
        icp_weight=0.75,
        opportunity_weight=0.25,
    )

    assert score == 75.0


def test_opportunity_weighted_higher():
    score = calculate_priority_score(
        icp_score=0,
        opportunity_score=100,
        icp_weight=0.25,
        opportunity_weight=0.75,
    )

    assert score == 75.0


def test_score_is_capped_at_100():
    score = calculate_priority_score(
        icp_score=100,
        opportunity_score=100,
        icp_weight=2,
        opportunity_weight=2,
    )

    assert score == 100.0


def test_zero_weights_rejected():
    with pytest.raises(ValueError):
        calculate_priority_score(
            icp_score=50,
            opportunity_score=50,
            icp_weight=0,
            opportunity_weight=0,
        )

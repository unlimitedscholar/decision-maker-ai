
from types import SimpleNamespace

from app.services.icp_scoring import (
    ICPConfig,
    calculate_icp_fit,
)


def make_company(**kwargs):
    defaults = {
        "industry": "SaaS",
        "employee_count": 200,
        "country": "United Kingdom",
        "revenue_range": "$10M-$50M",
    }

    defaults.update(kwargs)

    return SimpleNamespace(**defaults)


def test_perfect_icp_fit():
    company = make_company()

    profile = ICPConfig(
        industries=["SaaS"],
        min_employees=100,
        max_employees=500,
        countries=["United Kingdom"],
        revenue_ranges=["$10M-$50M"],
    )

    result = calculate_icp_fit(company, profile)

    assert result["score"] == 100.0


def test_wrong_industry():
    company = make_company(industry="Healthcare")

    profile = ICPConfig(
        industries=["SaaS"],
    )

    result = calculate_icp_fit(company, profile)

    assert result["components"]["industry"] == 0.0
    assert result["score"] < 100.0


def test_employee_range():
    company = make_company(employee_count=50)

    profile = ICPConfig(
        min_employees=100,
        max_employees=500,
    )

    result = calculate_icp_fit(company, profile)

    assert result["components"]["employees"] == 0.0


def test_missing_data():
    company = make_company(
        industry=None,
        employee_count=None,
        country=None,
        revenue_range=None,
    )

    profile = ICPConfig(
        industries=["SaaS"],
        min_employees=100,
        countries=["United Kingdom"],
        revenue_ranges=["$10M-$50M"],
    )

    result = calculate_icp_fit(company, profile)

    assert result["score"] == 0.0


def test_empty_profile():
    company = make_company()

    profile = ICPConfig()

    result = calculate_icp_fit(company, profile)

    assert result["score"] == 100.0


from dataclasses import dataclass
from typing import Optional


@dataclass
class ICPConfig:
    industries: Optional[list[str]] = None
    min_employees: Optional[int] = None
    max_employees: Optional[int] = None
    countries: Optional[list[str]] = None
    revenue_ranges: Optional[list[str]] = None


def calculate_icp_fit(company, profile: ICPConfig) -> dict:
    scores = {}

    # Industry
    if profile.industries:
        if company.industry:
            allowed = {
                value.lower()
                for value in profile.industries
            }

            scores["industry"] = (
                100.0
                if company.industry.lower() in allowed
                else 0.0
            )
        else:
            scores["industry"] = 0.0
    else:
        scores["industry"] = 100.0

    # Employee count
    if (
        profile.min_employees is not None
        or profile.max_employees is not None
    ):
        if company.employee_count is None:
            scores["employees"] = 0.0
        else:
            meets_min = (
                profile.min_employees is None
                or company.employee_count >= profile.min_employees
            )

            meets_max = (
                profile.max_employees is None
                or company.employee_count <= profile.max_employees
            )

            scores["employees"] = (
                100.0
                if meets_min and meets_max
                else 0.0
            )
    else:
        scores["employees"] = 100.0

    # Country
    if profile.countries:
        if company.country:
            allowed = {
                value.lower()
                for value in profile.countries
            }

            scores["country"] = (
                100.0
                if company.country.lower() in allowed
                else 0.0
            )
        else:
            scores["country"] = 0.0
    else:
        scores["country"] = 100.0

    # Revenue
    if profile.revenue_ranges:
        if company.revenue_range:
            allowed = {
                value.lower()
                for value in profile.revenue_ranges
            }

            scores["revenue"] = (
                100.0
                if company.revenue_range.lower() in allowed
                else 0.0
            )
        else:
            scores["revenue"] = 0.0
    else:
        scores["revenue"] = 100.0

    final_score = (
        scores["industry"] * 0.30
        + scores["employees"] * 0.25
        + scores["country"] * 0.20
        + scores["revenue"] * 0.25
    )

    return {
        "score": round(final_score, 2),
        "components": scores,
    }

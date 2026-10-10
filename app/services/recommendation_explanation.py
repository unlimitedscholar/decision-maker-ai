
def build_recommendation_explanation(
    recommendation: dict,
) -> dict:
    reasons = []

    icp_score = recommendation["icp_score"]
    opportunity_score = recommendation[
        "opportunity_score"
    ]

    # ICP explanation
    if icp_score >= 75:
        reasons.append(
            f"Strong ICP fit ({icp_score:.0f}/100)."
        )
    elif icp_score >= 45:
        reasons.append(
            f"Moderate ICP fit ({icp_score:.0f}/100)."
        )
    else:
        reasons.append(
            f"Weak ICP fit ({icp_score:.0f}/100)."
        )

    # Opportunity explanation
    if opportunity_score >= 75:
        reasons.append(
            f"Strong current opportunity "
            f"({opportunity_score:.0f}/100)."
        )
    elif opportunity_score >= 45:
        reasons.append(
            f"Moderate current opportunity "
            f"({opportunity_score:.0f}/100)."
        )
    else:
        reasons.append(
            f"Limited current opportunity "
            f"({opportunity_score:.0f}/100)."
        )

    # Strongest signal
    strongest_signal = recommendation.get(
        "strongest_signal"
    )

    if strongest_signal:
        reasons.append(
            "Strongest signal: "
            f"{strongest_signal['title']}."
        )

    # Signal count
    signal_count = recommendation.get(
        "signal_count",
        0,
    )

    if signal_count > 1:
        reasons.append(
            f"{signal_count} relevant signals detected."
        )
    elif signal_count == 1:
        reasons.append(
            "1 relevant signal detected."
        )
    else:
        reasons.append(
            "No relevant signals detected."
        )

    return {
        "recommendation": recommendation[
            "recommendation"
        ],
        "priority_score": recommendation[
            "priority_score"
        ],
        "reasons": reasons,
        "strongest_signal": strongest_signal,
    }

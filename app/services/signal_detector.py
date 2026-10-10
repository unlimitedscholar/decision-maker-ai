
from dataclasses import dataclass
from datetime import datetime
import re

from app.core.signal_types import (
    SignalType,
    SIGNAL_STRENGTH,
)


@dataclass
class DetectedSignal:
    signal_type: str
    title: str
    description: str
    confidence: float
    strength: int
    observed_at: datetime
    metadata_json: dict


def _contains_any(text: str, keywords: list[str]) -> bool:
    text = text.lower()

    return any(
        keyword.lower() in text
        for keyword in keywords
    )


def detect_signals(
    event_type: str,
    title: str | None,
    content: str | None,
    observed_at: datetime,
    metadata: dict | None = None,
) -> list[DetectedSignal]:

    title = title or ""
    content = content or ""

    text = f"{title} {content}".strip()

    signals: list[DetectedSignal] = []

    # ----------------------------------------
    # Hiring
    # ----------------------------------------

    if _contains_any(
        text,
        [
            "hiring",
            "hired",
            "new hires",
            "recruiting",
            "job openings",
            "open positions",
        ],
    ):

        signals.append(
            DetectedSignal(
                signal_type=SignalType.HIRING.value,
                title="Hiring activity detected",
                description=(
                    "The company appears to be increasing "
                    "hiring or recruiting activity."
                ),
                confidence=0.75,
                strength=SIGNAL_STRENGTH[SignalType.HIRING],
                observed_at=observed_at,
                metadata_json=metadata or {},
            )
        )

    # ----------------------------------------
    # Funding
    # ----------------------------------------

    if _contains_any(
        text,
        [
            "funding",
            "funded",
            "raised",
            "series a",
            "series b",
            "series c",
            "investment",
            "venture capital",
        ],
    ):

        signals.append(
            DetectedSignal(
                signal_type=SignalType.FUNDING.value,
                title="Funding activity detected",
                description=(
                    "The company appears to have received "
                    "new investment or funding."
                ),
                confidence=0.85,
                strength=SIGNAL_STRENGTH[SignalType.FUNDING],
                observed_at=observed_at,
                metadata_json=metadata or {},
            )
        )

    # ----------------------------------------
    # Leadership
    # ----------------------------------------

    if _contains_any(
        text,
        [
            "appointed",
            "joined as ceo",
            "joined as cfo",
            "joined as cro",
            "new ceo",
            "new cfo",
            "new cro",
            "chief revenue officer",
            "chief executive officer",
        ],
    ):

        signals.append(
            DetectedSignal(
                signal_type=SignalType.LEADERSHIP_CHANGE.value,
                title="Leadership change detected",
                description=(
                    "A potentially significant leadership "
                    "change was detected."
                ),
                confidence=0.80,
                strength=SIGNAL_STRENGTH[
                    SignalType.LEADERSHIP_CHANGE
                ],
                observed_at=observed_at,
                metadata_json=metadata or {},
            )
        )

    # ----------------------------------------
    # Expansion
    # ----------------------------------------

    if _contains_any(
        text,
        [
            "expanding",
            "expansion",
            "new office",
            "opened an office",
            "entered the market",
            "international expansion",
            "new market",
        ],
    ):

        signals.append(
            DetectedSignal(
                signal_type=SignalType.EXPANSION.value,
                title="Expansion activity detected",
                description=(
                    "The company appears to be expanding "
                    "into a new market or location."
                ),
                confidence=0.75,
                strength=SIGNAL_STRENGTH[
                    SignalType.EXPANSION
                ],
                observed_at=observed_at,
                metadata_json=metadata or {},
            )
        )

    # ----------------------------------------
    # Technology
    # ----------------------------------------

    if _contains_any(
        text,
        [
            "technology stack",
            "migrated to",
            "implemented",
            "adopted",
            "new software",
            "new platform",
            "technology migration",
        ],
    ):

        signals.append(
            DetectedSignal(
                signal_type=SignalType.TECHNOLOGY_CHANGE.value,
                title="Technology change detected",
                description=(
                    "The company appears to have changed "
                    "or adopted technology."
                ),
                confidence=0.65,
                strength=SIGNAL_STRENGTH[
                    SignalType.TECHNOLOGY_CHANGE
                ],
                observed_at=observed_at,
                metadata_json=metadata or {},
            )
        )

    # ----------------------------------------
    # Intent
    # ----------------------------------------

    if _contains_any(
        text,
        [
            "looking for",
            "evaluating",
            "considering",
            "request for proposal",
            "rfp",
            "vendor",
            "solution",
            "buying",
        ],
    ):

        signals.append(
            DetectedSignal(
                signal_type=SignalType.INTENT.value,
                title="Potential buying intent detected",
                description=(
                    "The event contains language suggesting "
                    "potential buying or vendor evaluation intent."
                ),
                confidence=0.60,
                strength=SIGNAL_STRENGTH[
                    SignalType.INTENT
                ],
                observed_at=observed_at,
                metadata_json=metadata or {},
            )
        )

    return signals

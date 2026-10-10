
import uuid

from sqlalchemy.orm import Session

from app.models.raw_event import RawEvent
from app.services.signal_detector import detect_signals
from app.services.company_signal_service import create_signal


def process_raw_event(
    session: Session,
    event: RawEvent,
):

    if not event.company_id:
        return []

    detected_signals = detect_signals(
        event_type=event.event_type,
        title=event.title,
        content=event.content,
        observed_at=event.observed_at,
        metadata=event.raw_metadata,
    )

    created_signals = []

    for detected in detected_signals:

        signal = create_signal(
            session=session,
            tenant_id=event.tenant_id,
            company_id=event.company_id,
            data={
                "signal_type": detected.signal_type,
                "title": detected.title,
                "description": detected.description,
                "source_type": event.source_type,
                "source_url": event.source_url,
                "source_name": event.source_name,
                "observed_at": detected.observed_at,
                "confidence": detected.confidence,
                "strength": detected.strength,
                "metadata_json": detected.metadata_json,
            },
        )

        created_signals.append(signal)

    return created_signals

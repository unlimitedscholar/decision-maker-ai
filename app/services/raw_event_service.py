
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.raw_event import RawEvent


def create_raw_event(
    session: Session,
    tenant_id: uuid.UUID,
    data: dict,
) -> RawEvent:

    event = RawEvent(
        tenant_id=tenant_id,
        **data,
    )

    session.add(event)
    session.commit()
    session.refresh(event)

    return event


def get_raw_event(
    session: Session,
    tenant_id: uuid.UUID,
    event_id: uuid.UUID,
) -> RawEvent | None:

    statement = select(RawEvent).where(
        RawEvent.id == event_id,
        RawEvent.tenant_id == tenant_id,
    )

    return session.scalar(statement)


def list_raw_events(
    session: Session,
    tenant_id: uuid.UUID,
) -> list[RawEvent]:

    statement = (
        select(RawEvent)
        .where(RawEvent.tenant_id == tenant_id)
        .order_by(RawEvent.observed_at.desc())
    )

    return list(
        session.scalars(statement).all()
    )

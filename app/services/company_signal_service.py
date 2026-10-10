
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.company_signal import CompanySignal


def create_signal(
    session: Session,
    tenant_id: uuid.UUID,
    company_id: uuid.UUID,
    data: dict,
) -> CompanySignal:

    signal = CompanySignal(
        tenant_id=tenant_id,
        company_id=company_id,
        **data,
    )

    session.add(signal)
    session.commit()
    session.refresh(signal)

    return signal


def get_signal(
    session: Session,
    tenant_id: uuid.UUID,
    company_id: uuid.UUID,
    signal_id: uuid.UUID,
) -> CompanySignal | None:

    statement = select(CompanySignal).where(
        CompanySignal.id == signal_id,
        CompanySignal.tenant_id == tenant_id,
        CompanySignal.company_id == company_id,
    )

    return session.scalar(statement)


def list_signals(
    session: Session,
    tenant_id: uuid.UUID,
    company_id: uuid.UUID,
) -> list[CompanySignal]:

    statement = (
        select(CompanySignal)
        .where(
            CompanySignal.tenant_id == tenant_id,
            CompanySignal.company_id == company_id,
        )
        .order_by(
            CompanySignal.observed_at.desc()
        )
    )

    return list(
        session.scalars(statement).all()
    )

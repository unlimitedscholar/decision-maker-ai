
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.company import Company


def create_company(
    session: Session,
    tenant_id: uuid.UUID,
    data: dict,
) -> Company:

    company = Company(
        tenant_id=tenant_id,
        **data,
    )

    session.add(company)
    session.commit()
    session.refresh(company)

    return company


def get_company(
    session: Session,
    tenant_id: uuid.UUID,
    company_id: uuid.UUID,
) -> Company | None:

    statement = select(Company).where(
        Company.id == company_id,
        Company.tenant_id == tenant_id,
    )

    return session.scalar(statement)


def list_companies(
    session: Session,
    tenant_id: uuid.UUID,
) -> list[Company]:

    statement = (
        select(Company)
        .where(Company.tenant_id == tenant_id)
        .order_by(Company.created_at.desc())
    )

    return list(session.scalars(statement).all())

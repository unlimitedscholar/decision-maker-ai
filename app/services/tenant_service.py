
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.identity import (
    Tenant,
    Membership,
    MembershipRole,
)


def create_tenant(
    session: Session,
    name: str,
    slug: str,
    owner_user_id: uuid.UUID,
):

    existing_tenant = session.scalar(
        select(Tenant).where(
            Tenant.slug == slug
        )
    )

    if existing_tenant:
        raise ValueError(
            "Tenant slug already exists"
        )

    tenant = Tenant(
        name=name,
        slug=slug,
    )

    session.add(tenant)
    session.flush()

    membership = Membership(
        user_id=owner_user_id,
        tenant_id=tenant.id,
        role=MembershipRole.OWNER,
    )

    session.add(membership)

    session.flush()

    return tenant, membership


def get_membership(
    session: Session,
    user_id: uuid.UUID,
    tenant_id: uuid.UUID,
):

    return session.scalar(
        select(Membership).where(
            Membership.user_id == user_id,
            Membership.tenant_id == tenant_id,
        )
    )

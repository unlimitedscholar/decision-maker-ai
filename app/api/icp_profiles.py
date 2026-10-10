import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.models.identity import User, Tenant
from app.models.icp_profile import ICPProfile
from app.schemas.icp_profile import (
    ICPProfileCreateRequest,
    ICPProfileResponse,
)
from app.services.tenant_service import get_membership


router = APIRouter(
    prefix="/tenants/{tenant_id}/icp-profiles",
    tags=["ICP Profiles"],
)


def verify_tenant_membership(
    session: Session,
    current_user: User,
    tenant_id: uuid.UUID,
):
    membership = get_membership(session, current_user.id, tenant_id)
    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this tenant",
        )
    return membership


@router.post(
    "",
    response_model=ICPProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_icp_profile(
    tenant_id: uuid.UUID,
    request: ICPProfileCreateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    verify_tenant_membership(session, current_user, tenant_id)

    tenant = session.get(Tenant, tenant_id)
    if tenant is None:
        raise HTTPException(status_code=404, detail="Tenant not found")

    profile = ICPProfile(
        tenant_id=tenant_id,
        **request.model_dump(),
    )
    session.add(profile)

    try:
        session.commit()
        session.refresh(profile)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An ICP profile with this name already exists for this tenant",
        )

    return profile


@router.get(
    "",
    response_model=list[ICPProfileResponse],
)
def list_icp_profiles(
    tenant_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):
    verify_tenant_membership(session, current_user, tenant_id)

    return session.scalars(
        select(ICPProfile)
        .where(ICPProfile.tenant_id == tenant_id)
        .order_by(ICPProfile.created_at.asc())
    ).all()

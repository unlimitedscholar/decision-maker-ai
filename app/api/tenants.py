
import uuid

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_db,
    get_current_user,
    require_tenant_role,
)

from app.models.identity import (
    User,
    Tenant,
    Membership,
    MembershipRole,
)

from app.schemas.identity import (
    TenantCreateRequest,
    TenantResponse,
    AddMemberRequest,
)

from app.services.tenant_service import (
    create_tenant,
)


router = APIRouter(
    prefix="/tenants",
    tags=["Tenants"],
)


@router.post(
    "",
    response_model=TenantResponse,
)
def create_company(
    request: TenantCreateRequest,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):

    try:

        tenant, membership = create_tenant(
            db,
            request.name,
            request.slug,
            current_user.id,
        )

        db.commit()
        db.refresh(tenant)

        return TenantResponse(
            id=str(tenant.id),
            name=tenant.name,
            slug=tenant.slug,
            role=membership.role.value,
        )

    except ValueError as error:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


@router.get("")
def list_tenants(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db),
):

    memberships = db.scalars(
        select(Membership).where(
            Membership.user_id == current_user.id
        )
    ).all()

    results = []

    for membership in memberships:

        tenant = db.get(
            Tenant,
            membership.tenant_id,
        )

        if tenant:

            results.append({
                "id": str(tenant.id),
                "name": tenant.name,
                "slug": tenant.slug,
                "role": membership.role.value,
            })

    return results


@router.get("/{tenant_id}")
def get_tenant(
    tenant_id: uuid.UUID,
    membership: Membership = Depends(
        require_tenant_role(
            MembershipRole.MEMBER
        )
    ),
    db: Session = Depends(get_db),
):

    tenant = db.get(
        Tenant,
        tenant_id,
    )

    if tenant is None:

        raise HTTPException(
            status_code=404,
            detail="Tenant not found",
        )

    return {
        "id": str(tenant.id),
        "name": tenant.name,
        "slug": tenant.slug,
        "role": membership.role.value,
    }


@router.post(
    "/{tenant_id}/members"
)
def add_member(
    tenant_id: uuid.UUID,
    request: AddMemberRequest,
    membership: Membership = Depends(
        require_tenant_role(
            MembershipRole.ADMIN
        )
    ),
    db: Session = Depends(get_db),
):

    user = db.scalar(
        select(User).where(
            User.email == request.email
        )
    )

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    existing = db.scalar(
        select(Membership).where(
            Membership.user_id == user.id,
            Membership.tenant_id == tenant_id,
        )
    )

    if existing:

        raise HTTPException(
            status_code=400,
            detail="User is already a member",
        )

    if (
        request.role == MembershipRole.OWNER
        and membership.role
        != MembershipRole.OWNER
    ):

        raise HTTPException(
            status_code=403,
            detail="Only owners can create owners",
        )

    new_membership = Membership(
        user_id=user.id,
        tenant_id=tenant_id,
        role=request.role,
    )

    db.add(new_membership)
    db.commit()

    return {
        "message": "Member added",
        "user_id": str(user.id),
        "tenant_id": str(tenant_id),
        "role": request.role.value,
    }

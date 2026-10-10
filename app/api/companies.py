
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.models.identity import User
from app.schemas.company import (
    CompanyCreateRequest,
    CompanyResponse,
)
from app.services.company_service import (
    create_company,
    get_company,
    list_companies,
)
from app.services.tenant_service import get_membership


router = APIRouter(
    prefix="/companies",
    tags=["Companies"],
)


@router.post(
    "/{tenant_id}",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_company_endpoint(
    tenant_id: uuid.UUID,
    request: CompanyCreateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):

    membership = get_membership(
        session,
        current_user.id,
        tenant_id,
    )

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this tenant",
        )

    company = create_company(
        session=session,
        tenant_id=tenant_id,
        data=request.model_dump(),
    )

    return company


@router.get(
    "/{tenant_id}",
    response_model=list[CompanyResponse],
)
def list_company_endpoint(
    tenant_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):

    membership = get_membership(
        session,
        current_user.id,
        tenant_id,
    )

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this tenant",
        )

    return list_companies(
        session,
        tenant_id,
    )


@router.get(
    "/{tenant_id}/{company_id}",
    response_model=CompanyResponse,
)
def get_company_endpoint(
    tenant_id: uuid.UUID,
    company_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):

    membership = get_membership(
        session,
        current_user.id,
        tenant_id,
    )

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this tenant",
        )

    company = get_company(
        session,
        tenant_id,
        company_id,
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    return company

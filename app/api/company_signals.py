
import uuid

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_db,
    get_current_user,
)

from app.models.identity import User

from app.schemas.company_signal import (
    CompanySignalCreateRequest,
    CompanySignalResponse,
)

from app.services.company_signal_service import (
    create_signal,
    get_signal,
    list_signals,
)

from app.services.company_service import (
    get_company,
)

from app.services.tenant_service import (
    get_membership,
)


router = APIRouter(
    prefix="/companies",
    tags=["Company Signals"],
)


def verify_company_access(
    session: Session,
    current_user: User,
    tenant_id: uuid.UUID,
    company_id: uuid.UUID,
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


@router.post(
    "/{tenant_id}/{company_id}/signals",
    response_model=CompanySignalResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_company_signal_endpoint(
    tenant_id: uuid.UUID,
    company_id: uuid.UUID,
    request: CompanySignalCreateRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):

    verify_company_access(
        session,
        current_user,
        tenant_id,
        company_id,
    )

    signal = create_signal(
        session=session,
        tenant_id=tenant_id,
        company_id=company_id,
        data=request.model_dump(),
    )

    return signal


@router.get(
    "/{tenant_id}/{company_id}/signals",
    response_model=list[CompanySignalResponse],
)
def list_company_signals_endpoint(
    tenant_id: uuid.UUID,
    company_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):

    verify_company_access(
        session,
        current_user,
        tenant_id,
        company_id,
    )

    return list_signals(
        session,
        tenant_id,
        company_id,
    )


@router.get(
    "/{tenant_id}/{company_id}/signals/{signal_id}",
    response_model=CompanySignalResponse,
)
def get_company_signal_endpoint(
    tenant_id: uuid.UUID,
    company_id: uuid.UUID,
    signal_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_db),
):

    verify_company_access(
        session,
        current_user,
        tenant_id,
        company_id,
    )

    signal = get_signal(
        session,
        tenant_id,
        company_id,
        signal_id,
    )

    if not signal:
        raise HTTPException(
            status_code=404,
            detail="Signal not found",
        )

    return signal

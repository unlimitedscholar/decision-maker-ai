
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import engine
from app.core.security import decode_access_token
from app.models.identity import (
    User,
    Membership,
    MembershipRole,
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)


def get_db():
    with Session(engine) as session:
        yield session


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID",
        )

    user = db.get(User, user_uuid)

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    return user


ROLE_LEVELS = {
    MembershipRole.MEMBER: 1,
    MembershipRole.ADMIN: 2,
    MembershipRole.OWNER: 3,
}


def require_tenant_role(
    minimum_role: MembershipRole,
):

    def dependency(
        tenant_id: uuid.UUID,
        current_user: User = Depends(
            get_current_user
        ),
        db: Session = Depends(get_db),
    ):

        membership = db.scalar(
            select(Membership).where(
                Membership.user_id == current_user.id,
                Membership.tenant_id == tenant_id,
            )
        )

        if membership is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this tenant",
            )

        if (
            ROLE_LEVELS[membership.role]
            < ROLE_LEVELS[minimum_role]
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return membership

    return dependency

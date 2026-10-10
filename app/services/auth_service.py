
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    hash_password,
    verify_password,
)

from app.models.identity import User


def create_user(
    session: Session,
    email: str,
    password: str,
    first_name: str,
    last_name: str,
):

    existing_user = session.scalar(
        select(User).where(
            User.email == email
        )
    )

    if existing_user:
        raise ValueError(
            "Email already registered"
        )

    user = User(
        email=email,
        password_hash=hash_password(password),
        first_name=first_name,
        last_name=last_name,
    )

    session.add(user)
    session.flush()

    return user


def authenticate_user(
    session: Session,
    email: str,
    password: str,
):

    user = session.scalar(
        select(User).where(
            User.email == email
        )
    )

    if user is None:
        return None

    if not user.is_active:
        return None

    if not verify_password(
        password,
        user.password_hash,
    ):
        return None

    return user

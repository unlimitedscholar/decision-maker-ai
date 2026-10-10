
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)

from app.models.identity import MembershipRole


class RegisterRequest(BaseModel):

    email: EmailStr

    password: str = Field(
        min_length=8
    )

    first_name: str = Field(
        min_length=1,
        max_length=100,
    )

    last_name: str = Field(
        min_length=1,
        max_length=100,
    )


class LoginRequest(BaseModel):

    email: EmailStr

    password: str


class TokenResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"


class UserResponse(BaseModel):

    id: str

    email: EmailStr

    first_name: str

    last_name: str


class TenantCreateRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=255,
    )

    slug: str = Field(
        min_length=2,
        max_length=100,
    )


class TenantResponse(BaseModel):

    id: str

    name: str

    slug: str

    role: str


class AddMemberRequest(BaseModel):

    email: EmailStr

    role: MembershipRole = (
        MembershipRole.MEMBER
    )

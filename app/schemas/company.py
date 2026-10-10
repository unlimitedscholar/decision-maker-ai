
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CompanyCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    domain: str | None = None
    website: str | None = None
    industry: str | None = None
    employee_count: int | None = Field(default=None, ge=0)
    revenue_range: str | None = None
    headquarters: str | None = None
    country: str | None = None
    description: str | None = None
    founded_year: int | None = Field(default=None, ge=1800, le=2100)
    linkedin_url: str | None = None


class CompanyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenant_id: uuid.UUID
    name: str
    domain: str | None
    website: str | None
    industry: str | None
    employee_count: int | None
    revenue_range: str | None
    headquarters: str | None
    country: str | None
    description: str | None
    founded_year: int | None
    linkedin_url: str | None
    status: str
    created_at: datetime
    updated_at: datetime

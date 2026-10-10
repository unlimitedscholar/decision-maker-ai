from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ICPProfileCreateRequest(BaseModel):
    name: str = Field(default="Default ICP", min_length=2, max_length=255)
    industries: list[str] = Field(default_factory=list)
    countries: list[str] = Field(default_factory=list)
    revenue_ranges: list[str] = Field(default_factory=list)
    min_employees: int | None = Field(default=None, ge=0)
    max_employees: int | None = Field(default=None, ge=0)
    icp_weight: float = Field(default=0.5, ge=0, le=1)
    opportunity_weight: float = Field(default=0.5, ge=0, le=1)

    @model_validator(mode="after")
    def validate_employee_range(self):
        if (
            self.min_employees is not None
            and self.max_employees is not None
            and self.min_employees > self.max_employees
        ):
            raise ValueError("min_employees cannot exceed max_employees")
        return self


class ICPProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    tenant_id: UUID
    name: str
    industries: list[str]
    countries: list[str]
    revenue_ranges: list[str]
    min_employees: int | None
    max_employees: int | None
    icp_weight: float
    opportunity_weight: float
    created_at: datetime
    updated_at: datetime

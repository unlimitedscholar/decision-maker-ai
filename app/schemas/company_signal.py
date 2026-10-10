
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CompanySignalCreateRequest(BaseModel):
    signal_type: str = Field(min_length=1, max_length=100)

    title: str = Field(
        min_length=1,
        max_length=500
    )

    description: str | None = None

    source_type: str | None = None

    source_url: str | None = None

    source_name: str | None = None

    observed_at: datetime

    confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0
    )

    strength: int = Field(
        default=50,
        ge=0,
        le=100
    )

    metadata_json: dict | None = None


class CompanySignalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID

    tenant_id: uuid.UUID

    company_id: uuid.UUID

    signal_type: str

    title: str

    description: str | None

    source_type: str | None

    source_url: str | None

    source_name: str | None

    observed_at: datetime

    detected_at: datetime

    confidence: float

    strength: int

    metadata_json: dict | None

    created_at: datetime

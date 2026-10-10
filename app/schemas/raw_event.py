
import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class RawEventCreateRequest(BaseModel):
    company_id: uuid.UUID | None = None

    event_type: str = Field(
        min_length=1,
        max_length=100
    )

    title: str | None = None

    content: str | None = None

    source_type: str | None = None

    source_url: str | None = None

    source_name: str | None = None

    observed_at: datetime

    raw_metadata: dict | None = None


class RawEventResponse(BaseModel):
    id: uuid.UUID
    tenant_id: uuid.UUID
    company_id: uuid.UUID | None

    event_type: str

    title: str | None
    content: str | None

    source_type: str | None
    source_url: str | None
    source_name: str | None

    observed_at: datetime

    raw_metadata: dict | None

    created_at: datetime

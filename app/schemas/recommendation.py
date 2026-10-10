
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RecommendationResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    company_id: UUID
    icp_profile_id: UUID | None
    recommendation: str
    priority_score: float
    icp_score: float
    opportunity_score: float
    reasons: list[str]
    evidence: list[dict]
    model_version: str
    confidence: float | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

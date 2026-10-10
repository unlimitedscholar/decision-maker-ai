
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    JSON,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Recommendation(Base):
    __tablename__ = "recommendations"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenants.id"),
        nullable=False,
        index=True,
    )

    company_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
    )

    icp_profile_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("icp_profiles.id"),
        nullable=True,
        index=True,
    )

    recommendation: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    priority_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    icp_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    opportunity_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    reasons: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    evidence: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    model_version: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="baseline-v1",
    )

    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

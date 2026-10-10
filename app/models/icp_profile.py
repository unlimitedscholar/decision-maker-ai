
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ICPProfile(Base):
    __tablename__ = "icp_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenants.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        default="Default ICP",
    )

    industries: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    countries: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    revenue_ranges: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    min_employees: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    max_employees: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    icp_weight: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.50,
    )

    opportunity_weight: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.50,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "name",
            name="uq_icp_profile_tenant_name",
        ),
    )

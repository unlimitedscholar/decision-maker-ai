
import uuid
from datetime import datetime, timezone

from sqlalchemy import String, Integer, Text, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    domain: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True
    )

    website: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    industry: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    employee_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    revenue_range: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    headquarters: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    country: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    founded_year: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    linkedin_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="active"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    __table_args__ = (
        Index(
            "ix_companies_tenant_domain",
            "tenant_id",
            "domain",
            unique=True
        ),
    )

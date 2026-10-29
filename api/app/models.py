from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, index=True
    )
    external_id: Mapped[str | None] = mapped_column(
        String(100), nullable=True, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50), default="open", nullable=False
    )
    assigned_to: Mapped[str | None] = mapped_column(
        String(150), nullable=True, index=True
    )
    outcome: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
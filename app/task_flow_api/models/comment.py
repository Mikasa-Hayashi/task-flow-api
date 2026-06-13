import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from auth_kit.db.session import Base
from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from task_flow_api.models.task import Task


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[str] = mapped_column(
        String, primary_key=True, default=lambda: str(uuid.uuid4())
    )
    task_id: Mapped[str] = mapped_column(String, ForeignKey("tasks.id"), nullable=False)
    author_id: Mapped[str] = mapped_column(
        String, ForeignKey("users.id"), nullable=False
    )
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    task: Mapped["Task"] = relationship(back_populates="comments")

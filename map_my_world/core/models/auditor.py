from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from core.models.base import Base
from datetime import datetime


class Auditor(Base):
    __abstract__ = True

    date_created: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), nullable=False
    )
    date_updated: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now(), nullable=False
    )

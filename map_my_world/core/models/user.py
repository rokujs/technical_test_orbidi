from core.models.auditor import Auditor
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Auditor):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="users")

    def __repr__(self) -> str:
        return f"<User(username={self.username}, email={self.email})>"

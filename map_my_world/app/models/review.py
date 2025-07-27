from core.models.auditor import Auditor
from app.models.category import Category
from app.models.location import Location
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import Text, Integer, CheckConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from core.models.user import User


class Review(Auditor):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    review: Mapped[str | None] = mapped_column(Text, nullable=True)
    rating: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("rating >= 1 AND rating <= 5", name="check_rating_range"),
    )

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id")
    )

    categories: Mapped[list[Category]] = relationship(
        "Category", back_populates="reviews"
    )
    locations: Mapped[list[Location]] = relationship(
        "Location", back_populates="reviews"
    )
    users: Mapped[list[User]] = relationship("User", back_populates="reviews")

    def __repr__(self) -> str:
        return f"<Review(id={self.id}, rating={self.rating}, review={self.review})>"

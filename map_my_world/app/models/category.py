from core.models.auditor import Auditor
from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Category(Auditor):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviews: Mapped[list["Review"]] = relationship(
        "Review", back_populates="categories"
    )

    def __repr__(self) -> str:
        return f"<Category(name={self.name}, description={self.description})>"

from core.models.auditor import Auditor
from sqlalchemy import String, Text, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Location(Auditor):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="locations")

    def __repr__(self) -> str:
        return f"<Location(name={self.name}, latitude={self.latitude}, longitude={self.longitude})>"

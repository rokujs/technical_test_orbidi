from pydantic import BaseModel
import uuid


class ReviewSchema(BaseModel):
    id: int
    review: str | None = None
    rating: int
    category_id: int
    location_id: int
    user_id: uuid.UUID

    class Config:
        from_attributes = True

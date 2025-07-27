from pydantic import BaseModel

from app.schemas.category_schema import CategoryList
from app.schemas.location_schema import LocationList
from app.schemas.review_schema import ReviewSchema

class SuggestionSchema(BaseModel):
    location: LocationList
    category: CategoryList
    reviews: list[ReviewSchema] | None = None


class SuggestionParams(BaseModel):
    latitude: float
    longitude: float
    category_id: int
    page: int = 0
    limit: int = 10
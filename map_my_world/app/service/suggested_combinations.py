from datetime import datetime, timedelta, timezone
from sqlalchemy import func
from sqlalchemy.sql.expression import ColumnElement
from sqlalchemy.orm import Session

from app.models.location import Location
from app.models.review import Review
from app.schemas.suggestion_schema import SuggestionSchema
from app.models.category import Category


class SuggestedCombinations:
    RADIUS_METERS = 50.0
    EARTH_RADIUS_KM = 6371.0

    def __init__(
        self,
        db: Session,
        latitude: float,
        longitude: float,
        category_id: int,
        page: int = 0,
        limit: int = 10,
    ):
        self.db = db
        self.latitude = latitude
        self.longitude = longitude
        self.category_id = category_id
        self.page = page
        self.limit = limit

    def _get_haversine_distance_filter(self) -> ColumnElement:
        """
        Returns the Haversine distance filter to use in SQLAlchemy queries.
        """
        user_lat_rad = func.radians(self.latitude)
        user_lon_rad = func.radians(self.longitude)
        location_lat_rad = func.radians(Location.latitude)
        location_lon_rad = func.radians(Location.longitude)
        delta_lat = location_lat_rad - user_lat_rad
        delta_lon = location_lon_rad - user_lon_rad

        # Haversine formula to calculate the distance
        haversine_a = func.pow(func.sin(delta_lat / 2), 2) + func.cos(
            user_lat_rad
        ) * func.cos(location_lat_rad) * func.pow(func.sin(delta_lon / 2), 2)
        haversine_c = 2 * func.atan2(func.sqrt(haversine_a), func.sqrt(1 - haversine_a))

        distance_km = self.EARTH_RADIUS_KM * haversine_c

        return distance_km <= self.RADIUS_METERS

    def _get_location_within_radius(self) -> list[Location]:
        """
        Fetches suggested combinations of locations and categories within a specified radius.
        Orders: 1) Locations without reviews, 2) Locations with reviews older than 30 days.
        """
        distance_filter = self._get_haversine_distance_filter()
        # Subquery to get reviews for each location, using date_created from Review
        review_subq = self.db.query(Review.location_id, Review.date_created).subquery()

        # 30 days ago
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)

        # Annotate locations with review date_created (if any)
        query = (
            self.db.query(Location)
            .outerjoin(review_subq, review_subq.c.location_id == Location.id)
            .filter(distance_filter)
            .order_by(
                # First those without review (date_created is None), then those with reviews older than 30 days
                (review_subq.c.date_created.is_(None)).desc(),
                (review_subq.c.date_created < thirty_days_ago).desc(),
            )
        )
        offset = self.page * self.limit
        locations = query.offset(offset).limit(self.limit).all()
        return locations

    def _get_category_for_location(
        self, location: Location
    ) -> tuple[Category, list[Review]]:
        """
        For a given location, returns:
        - the category that matches the location and self.category_id in Review (if exists), otherwise a random category for that location
        - a list of reviews for that location and category
        """
        reviews = (
            self.db.query(Review)
            .filter(
                (Review.location_id == location.id)
                & (Review.category_id == self.category_id)
            )
            .order_by(Review.date_created.desc())
            .limit(10)
            .all()
        )
        if reviews:
            category = (
                self.db.query(Category).filter(Category.id == self.category_id).first()
            )
        else:
            category = self.db.query(Category).order_by(func.random()).first()
        return category, reviews

    def get_suggestions(self) -> list[SuggestionSchema]:
        locations = self._get_location_within_radius()
        suggestions = []

        for location in locations:
            category, reviews = self._get_category_for_location(location)
            suggestion = SuggestionSchema(
                location=location, category=category, reviews=reviews
            )
            suggestions.append(suggestion)
        return suggestions

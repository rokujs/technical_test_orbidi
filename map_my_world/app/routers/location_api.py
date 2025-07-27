from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from app.models.location import Location
from app.schemas.location_schema import LocationCreate, LocationList

router = APIRouter(prefix="/location", tags=["Locations"])


@router.post("/", response_model=LocationList, status_code=status.HTTP_201_CREATED)
async def create_location(item: LocationCreate, db: Session = Depends(get_db)):
    # Normalize the name: all lowercase
    normalized_name = item.name.strip().capitalize()
    # Check if a location with that name already exists
    existing = db.query(Location).filter(Location.name == normalized_name).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Location already exists"
        )

    location = Location(
        name=normalized_name,
        description=item.description,
        latitude=item.latitude,
        longitude=item.longitude,
    )

    db.add(location)
    db.commit()
    db.refresh(location)

    return location


@router.get("/", response_model=list[LocationList])
async def list_locations(db: Session = Depends(get_db)):
    locations = db.query(Location).order_by(Location.date_created.desc()).all()
    return locations

from pydantic import BaseModel

class LocationBase(BaseModel):
    name: str
    description: str | None = None
    latitude: float
    longitude: float

class LocationCreate(LocationBase):
    pass

class LocationList(LocationBase):
    id: int

    class Config:
        from_attributes = True

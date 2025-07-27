from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: str | None = None

class CategoryCreate(CategoryBase):
    pass

class CategoryList(CategoryBase):
    id: int

    class Config:
        from_attributes = True

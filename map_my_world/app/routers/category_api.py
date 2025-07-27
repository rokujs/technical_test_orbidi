from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from app.models.category import Category
from app.schemas.category_schema import CategoryCreate, CategoryList

router = APIRouter(prefix="/category", tags=["Categories"])


@router.post("/", response_model=CategoryList, status_code=status.HTTP_201_CREATED)
async def create_category(item: CategoryCreate, db: Session = Depends(get_db)):
    # Normalize the name
    normalized_name = item.name.strip().capitalize()
    # Check if a category with that name already exists
    existing = db.query(Category).filter(Category.name == normalized_name).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Category already exists"
        )

    category = Category(name=normalized_name, description=item.description)

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


@router.get("/", response_model=list[CategoryList])
async def list_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).order_by(Category.date_created.desc()).all()
    return categories

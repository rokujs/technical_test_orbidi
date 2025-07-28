from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from app.schemas.suggestion_schema import SuggestionParams, SuggestionSchema

router = APIRouter(prefix="/suggestions", tags=["Suggestions"])


@router.get("/", response_model=list[SuggestionSchema])
async def list_suggestions(
    params: SuggestionParams = Depends(), db: Session = Depends(get_db)
):
    from app.service.suggested_combinations import SuggestedCombinations

    sc = SuggestedCombinations(
        db,
        params.latitude,
        params.longitude,
        params.category_id,
        params.page,
        params.limit,
    )
    suggestions = sc.get_suggestions()
    return suggestions

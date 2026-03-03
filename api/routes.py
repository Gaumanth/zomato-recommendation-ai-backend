from fastapi import APIRouter, HTTPException
from models.preferences import (
    UserPreferences,
    RecommendationResponse,
    MetadataResponse,
)
from data.data_loader import get_dataframe, get_unique_cities, get_unique_cuisines
from services.filter_service import filter_restaurants
from services.llm_service import get_llm_recommendation

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.get("/metadata", response_model=MetadataResponse)
async def get_metadata():
    """Return available cities, cuisines, and restaurant count for the frontend dropdowns."""
    try:
        df = get_dataframe()
        return MetadataResponse(
            cities=get_unique_cities(df),
            cuisines=get_unique_cuisines(df),
            total_restaurants=len(df),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load metadata: {str(e)}")


@router.post("/recommend", response_model=RecommendationResponse)
async def recommend(prefs: UserPreferences):
    """Accept user preferences, filter restaurants, call LLM, and return recommendations."""
    try:
        df = get_dataframe()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load data: {str(e)}")

    filtered = filter_restaurants(df, prefs, top_n=10)

    summary = await get_llm_recommendation(prefs, filtered)

    return RecommendationResponse(
        summary=summary,
        restaurants=filtered,
        filtered_count=len(filtered),
    )

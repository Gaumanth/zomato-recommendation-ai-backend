from pydantic import BaseModel, Field


class UserPreferences(BaseModel):
    place: str = Field(default="", description="City or location name")
    cuisine: str = Field(default="", description="Preferred cuisine type")
    price: str = Field(default="", description="Budget: low, medium, or high")
    rating: float = Field(default=0.0, ge=0.0, le=5.0, description="Minimum rating (0-5)")


class RestaurantItem(BaseModel):
    name: str
    cuisines: str
    rating: float
    cost_for_two: float
    city: str
    price_category: str = ""


class RecommendationResponse(BaseModel):
    summary: str
    restaurants: list[RestaurantItem]
    filtered_count: int = 0


class MetadataResponse(BaseModel):
    cities: list[str]
    cuisines: list[str]
    total_restaurants: int

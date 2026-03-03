import pandas as pd
from models.preferences import UserPreferences, RestaurantItem


def categorize_price(cost: float) -> str:
    """Categorize cost_for_two into low / medium / high buckets."""
    if cost <= 300:
        return "low"
    elif cost <= 800:
        return "medium"
    return "high"


def filter_restaurants(
    df: pd.DataFrame,
    prefs: UserPreferences,
    top_n: int = 10,
) -> list[RestaurantItem]:
    """Filter and rank restaurants based on user preferences."""
    filtered = df.copy()

    filtered["price_category"] = filtered["cost_for_two"].apply(categorize_price)

    if prefs.place:
        place_lower = prefs.place.lower()
        filtered = filtered[filtered["city"].str.lower().str.contains(place_lower, na=False)]

    if prefs.cuisine:
        cuisine_lower = prefs.cuisine.lower()
        filtered = filtered[filtered["cuisines"].str.lower().str.contains(cuisine_lower, na=False)]

    if prefs.price:
        filtered = filtered[filtered["price_category"] == prefs.price.lower()]

    if prefs.rating > 0:
        filtered = filtered[filtered["rating"] >= prefs.rating]

    filtered = filtered.drop_duplicates(subset=["name", "city"], keep="first")

    filtered = filtered.sort_values(by=["rating", "cost_for_two"], ascending=[False, True])

    top = filtered.head(top_n)

    results: list[RestaurantItem] = []
    for _, row in top.iterrows():
        results.append(
            RestaurantItem(
                name=str(row.get("name", "")),
                cuisines=str(row.get("cuisines", "")),
                rating=float(row.get("rating", 0)),
                cost_for_two=float(row.get("cost_for_two", 0)),
                city=str(row.get("city", "")),
                price_category=categorize_price(float(row.get("cost_for_two", 0))),
            )
        )

    return results

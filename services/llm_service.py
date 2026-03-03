import os
import google.generativeai as genai
from dotenv import load_dotenv
from models.preferences import UserPreferences, RestaurantItem

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))

PROMPT_TEMPLATE = """You are a friendly and knowledgeable restaurant recommendation assistant.

A user is looking for restaurant recommendations with the following preferences:
- Location: {place}
- Cuisine: {cuisine}
- Budget: {price}
- Minimum Rating: {rating}

Here are the top matching restaurants from our Zomato database:

{restaurant_list}

Based on these results, please:
1. Recommend the top 3-5 restaurants from the list above.
2. For each, explain briefly WHY it's a great pick for this user.
3. Include the restaurant name, cuisine type, rating, approximate cost for two, and city.
4. If few results match, acknowledge that and still give the best options.
5. Keep the tone conversational and helpful.

Format your response as a clear, readable summary."""


def build_restaurant_list(restaurants: list[RestaurantItem]) -> str:
    lines = []
    for i, r in enumerate(restaurants, 1):
        lines.append(
            f"{i}. {r.name} | Cuisine: {r.cuisines} | Rating: {r.rating}/5 | "
            f"Cost for Two: ₹{r.cost_for_two:.0f} | City: {r.city} | Budget: {r.price_category}"
        )
    return "\n".join(lines)


async def get_llm_recommendation(
    prefs: UserPreferences,
    restaurants: list[RestaurantItem],
) -> str:
    """Send filtered restaurants + user prefs to Gemini and get a recommendation summary."""
    if not restaurants:
        return "No restaurants matched your criteria. Try adjusting your filters for better results."

    restaurant_list = build_restaurant_list(restaurants)

    prompt = PROMPT_TEMPLATE.format(
        place=prefs.place or "Any",
        cuisine=prefs.cuisine or "Any",
        price=prefs.price or "Any",
        rating=prefs.rating,
        restaurant_list=restaurant_list,
    )

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        return (
            f"I found {len(restaurants)} matching restaurants but couldn't generate "
            f"a personalized summary right now. Error: {str(e)}\n\n"
            f"Here are the top picks:\n{restaurant_list}"
        )

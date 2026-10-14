# =====================================================================
# models/nutrition.py — USDA FoodData Central (open data, no LLM)
# =====================================================================
import httpx

FDC_API = "https://api.nal.usda.gov/fdc/v1/foods/search"
IRONSRC = ["tofu", "lentils", "tempeh", "oats", "spinach", "chickpeas"]


class NutritionDB:
    def __init__(self, api_key: str):
        self.http = httpx.AsyncClient(timeout=10)
        self.cache = {}  # name -> per-100g dict; also Postgres-backed

    async def per_100g(self, ingredient: str) -> dict:
        if ingredient not in self.cache:
            r = await self.http.get(FDC_API, params={
                "query": ingredient, "api_key": self.api_key, "pageSize": 1
            })
            food = r.json()["foods"][0]
            nutrients = {n["nutrientName"]: n["value"]
                         for n in food["foodNutrients"]}
            self.cache[ingredient] = {
                "kcal": nutrients.get("Energy", 0),
                "protein_g": nutrients.get("Protein", 0),
                "iron_mg": nutrients.get("Iron, Fe", 0),
                "b12_ug": nutrients.get("Vitamin B-12", 0),  # ~0 in plants -> we fortify via plan
            }
        return self.cache[ingredient]

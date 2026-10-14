# =====================================================================
# models/co2e.py — CO2e factors from public LCA datasets (Poore & Nemecek)
# =====================================================================
# kg CO2e per kg of food, cradle-to-retail. Fallback: category median.
CO2E_TABLE = {
    "tofu": 3.2, "tempeh": 2.5, "lentils": 0.9, "chickpeas": 0.8,
    "oats": 2.5, "rice": 4.5, "potatoes": 0.5, "spinach": 0.4,
    "kale": 0.4, "tomatoes": 2.1, "avocado": 2.5, "almonds": 3.6,
    "oat_milk": 0.6, "wheat_flour": 1.6, "bananas": 0.9,
}
CATEGORY_MEDIAN = {"legume": 1.0, "grain": 1.8, "vegetable": 0.5,
                   "fruit": 1.0, "nut": 3.5, "processed": 3.0}


class CO2DB:
    def kg_co2e_per_kg(self, ingredient: str) -> float:
        return CO2E_TABLE.get(ingredient) or CATEGORY_MEDIAN[self._category(ingredient)]

    def _category(self, ingredient: str) -> str: ...


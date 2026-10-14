# =====================================================================
# models/seasonality.py — EU-region seasonality tables
# =====================================================================
# Simplified: month -> in-season vegetables for a temperate EU region.
SEASON = {
    10: ["kale", "pumpkin", "beets", "carrots", "leek", "mushrooms", "apples"],
    # ... remaining months
}


def is_in_season(ingredient: str, region: str, month: int) -> bool:
    if region not in REGIONS:  # unknown region -> permissive
        return True
    return ingredient in SEASON.get(month, [])

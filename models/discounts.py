# =====================================================================
# models/discounts.py — weekly supermarket discount scraper (per region)
# =====================================================================
class DiscountScraper:
    def __init__(self, postgres):
        self.pg = postgres  # cached weekly, per region

    async def fetch(self, region: str) -> list[dict]:
        rows = await self.pg.fetch(
            "SELECT item, price, valid_until FROM discounts "
            "WHERE region = $1 AND valid_until >= now()", region)
        return [dict(r) for r in rows]

    async def refresh(self, region: str):
        """Runs weekly via the scheduler: hits retailer APIs, normalizes
        item names against our ingredient taxonomy, upserts."""
        ...

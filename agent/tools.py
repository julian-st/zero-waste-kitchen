# =====================================================================
# agent/tools.py — tools the agent can call (PydanticAI Tool wrappers)
# =====================================================================
from pydantic_ai import Agent, RunContext
from models.nutrition import NutritionDB
from models.co2e import CO2DB
from models.seasonality import is_in_season
from models.discounts import DiscountScraper


def build_agent(db: NutritionDB, co2: CO2DB, scraper: DiscountScraper) -> Agent:
    """Wires the open-weight model (Ollama) with typed tools."""

    agent = Agent(
        "ollama_chat:qwen2.5:14b",  # local Ollama; base_url set via OLLAMA_BASE_URL
        deps_type=Deps,
        output_type=list[MealProposal],
        retries=3,  # failed schema validation => automatic retry with error fed back
    )

    @agent.tool
    async def lookup_nutrition(ctx: RunContext[Deps], ingredient: str) -> dict:
        """USDA FoodData Central lookup: kcal, protein, iron, B12 per 100 g."""
        return db.per_100g(ingredient)

    @agent.tool
    async def lookup_co2e(ctx: RunContext[Deps], ingredient: str) -> float:
        """Life-cycle CO2e (kg) per kg of ingredient."""
        return co2.kg_co2e_per_kg(ingredient)

    @agent.tool
    async def check_seasonality(ctx: RunContext[Deps], ingredient: str, region: str) -> bool:
        return is_in_season(ingredient, region, month=ctx.deps.month)

    @agent.tool
    async def current_discounts(ctx: RunContext[Deps], region: str) -> list[dict]:
        """This week's local supermarket discounts, scraped & cached."""
        return await scraper.fetch(region)

    return agent

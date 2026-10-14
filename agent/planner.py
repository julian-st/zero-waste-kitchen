
# =====================================================================
# agent/planner.py — LLM proposes, LP solver disposes
# =====================================================================
import pulp
from .tools import build_agent
from .schemas import MealProposal, MealPlan


class Planner:
    def __init__(self, agent, nutrition_db, co2_db):
        self.agent = agent
        self.nutrition_db = nutrition_db
        self.co2_db = co2_db

    async def propose_candidates(self, pantry: list[str], region: str, month: int) -> list[MealProposal]:
        prompt = (
            "Propose 12 diverse vegan meal candidates.\n"
            f"PANTRY (use these first): {', '.join(pantry)}.\n"
            f"Region: {region}, month: {month} — call the seasonality tool before "
            "suggesting fresh produce. Call the discounts tool and prefer "
            "discounted items. Do NOT invent nutrition numbers."
        )
        return await self.agent.run(prompt)

    def optimize(self, candidates: list[MealProposal], targets: dict) -> MealPlan:
        """Linear program: choose meals minimizing cost + CO2e + waste,
        subject to weekly nutrition targets. Deterministic — no LLM here."""
        prob = pulp.LpProblem("meal_plan", pulp.LpMinimize)
        x = {m.title: pulp.LpVariable(f"x_{i}", cat="Binary")
             for i, m in enumerate(candidates)}

        # objective: cost + CO2e + penalty for ingredients used in only one meal
        prob += pulp.lpSum(
            x[m.title] * (self._cost(m) + self._co2(m) + 2.0 * self._orphan_score(m))
            for m in candidates
        )

        # constraints: nutrition targets
        for nutrient, (lo, hi) in targets.items():
            prob += lo <= pulp.lpSum(x[m.title] * self._nutrient(m, nutrient)
                                     for m in candidates) <= hi

        # meals per week
        prob += pulp.lpSum(x.values()) == 14  # 2/day for a 7-day plan

        prob.solve(pulp.PULP_CBC_CMD(msg=False))
        chosen = [m for m in candidates if x[m.title].value() == 1]

        return MealPlan(
            meals=chosen,
            pantry_used=sorted({i.name for m in chosen for i in m.ingredients}),
            grocery_list=self._merge_groceries(chosen),
            solver_notes=f"status={pulp.LpStatus[prob.status]}",
        )

    # --- cost / CO2 / nutrient helpers use the ground-truth DBs, not the LLM
    def _cost(self, meal): ...
    def _co2(self, meal): ...
    def _nutrient(self, meal, nutrient): ...
    def _orphan_score(self, meal): ...
    def _merge_groceries(self, meals): ...

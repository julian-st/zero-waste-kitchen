# =====================================================================
# agent/schemas.py
# Strict Pydantic schemas — the LLM output is validated, never trusted.
# =====================================================================
from typing import Literal
from pydantic import BaseModel, Field, field_validator


class Ingredient(BaseModel):
    name: str
    quantity_g: float = Field(gt=0, le=5000)
    unit: Literal["g", "ml", "piece"] = "g"


class MealProposal(BaseModel):
    """One candidate meal proposed by the LLM. No macros here — the LLM
    does NOT invent nutrition numbers; we compute them from ingredients."""
    title: str
    meal_type: Literal["breakfast", "lunch", "dinner", "snack"]
    ingredients: list[Ingredient]
    tags: list[str] = Field(default_factory=list)  # e.g. ["high-protein", "batch"]
    instructions: str = Field(min_length=20, max_length=3000)

    @field_validator("ingredients")
    @classmethod
    def non_empty(cls, v: list[Ingredient]) -> list[Ingredient]:
        if len(v) < 2:
            raise ValueError("a meal needs at least 2 ingredients")
        return v


class MealPlan(BaseModel):
    """The final, validated output of one planning session."""
    meals: list[MealProposal] = Field(min_length=3, max_length=21)
    pantry_used: list[str]
    grocery_list: list[Ingredient]
    solver_notes: str  # human-readable summary from the LP solver

    def total_unique_ingredients(self) -> int:
        return len({i.name for m in self.meals for i in m.ingredients})

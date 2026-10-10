import json
from pathlib import Path

from screening.poverty_guidelines import fpl_percentage

DATA_FILE = Path(__file__).parent.parent / "Data" / "programs.json"

with open(DATA_FILE) as f:
    PROGRAM_DATA = json.load(f)

PROGRAMS = PROGRAM_DATA["programs"]
def check_rule(rule, household):
    if rule["type"] == "income_below_fpl_pct":
        limit_pct = rule["value"]
        percent = fpl_percentage(household["annual_income"], household["size"])
        explanation = (
            f"Your household of {household['size']} is at {percent:.0f}% "
            f"of the poverty line. This program allows up to {limit_pct}%."
        )
        return percent <= limit_pct, explanation

    elif rule["type"] == "income_below_annual_limit_by_size":
        size = household["size"]
        if size < 1:
            raise ValueError(f"Household size must be at least 1, got {size}")
        if household["annual_income"] < 0:
            raise ValueError("Annual income must be a non-negative number")

        limits = rule["value"]["limits_by_size"]
        limit = limits.get(str(size))
        if limit is None:
            largest_size = max(int(limit_size) for limit_size in limits)
            if size < largest_size:
                raise ValueError(f"No income limit configured for household size {size}")
            limit = limits[str(largest_size)] + (
                size - largest_size
            ) * rule["value"]["additional_person_limit"]

        qualifies = household["annual_income"] <= limit
        explanation = (
            f"Your household of {size} has annual income of "
            f"${household['annual_income']:,.0f}. This program allows up to "
            f"${limit:,.0f}."
        )
        return qualifies, explanation

    elif rule["type"] == "has_child_under":
        max_age = rule["value"]
        has_child = False
        for age in household["ages"]:
            if age < max_age:
                has_child = True

        if has_child:
            explanation = f"There is someone under {max_age} in your household."
        else:
            explanation = f"This program requires someone under {max_age} in the household."
        return has_child, explanation

    elif rule["type"] == "state_residency":
        state = rule["value"]
        lives_here = household["state"] == state
        explanation = f"This program is only for residents of {state}."
        return lives_here, explanation

    else:
        raise ValueError(f"Unknown rule type: {rule['type']}")

print(PROGRAMS)
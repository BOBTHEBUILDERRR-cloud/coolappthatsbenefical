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

    elif rule["type"] == "income_between_annual_limits_by_size":
        size = household["size"]
        if size < 1:
            raise ValueError(f"Household size must be at least 1, got {size}")
        if household["annual_income"] < 0:
            raise ValueError("Annual income must be a non-negative number")

        value = rule["value"]
        minimum_limits = value["minimum_limits_by_size"]
        maximum_limits = value["maximum_limits_by_size"]
        minimum_limit = minimum_limits.get(str(size))
        maximum_limit = maximum_limits.get(str(size))
        if minimum_limit is None or maximum_limit is None:
            largest_size = min(
                max(int(limit_size) for limit_size in minimum_limits),
                max(int(limit_size) for limit_size in maximum_limits),
            )
            if size < largest_size:
                raise ValueError(f"No income limits configured for household size {size}")
            minimum_limit = minimum_limits[str(largest_size)] + (
                size - largest_size
            ) * value["additional_person_minimum_limit"]
            maximum_limit = maximum_limits[str(largest_size)] + (
                size - largest_size
            ) * value["additional_person_maximum_limit"]

        qualifies = minimum_limit <= household["annual_income"] <= maximum_limit
        explanation = (
            f"Your household of {size} has annual income of "
            f"${household['annual_income']:,.0f}. This program allows income "
            f"from ${minimum_limit:,.0f} through ${maximum_limit:,.0f}."
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
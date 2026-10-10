"""
Federal poverty guideline math.

Source: U.S. Department of Health and Human Services, Office of the Assistant
Secretary for Planning and Evaluation (ASPE).
https://aspe.hhs.gov/topics/poverty-economic-mobility/poverty-guidelines

2026 guidelines, effective January 13, 2026. These figures are for the 48
contiguous states and DC(Alaska and Hawaii not included).
"""

POVERTY_GUIDELINES_2026 = {
    "year": 2026,
    "region": "48 contiguous states and DC",
    "source_url": "https://aspe.hhs.gov/topics/poverty-economic-mobility/poverty-guidelines",
    "retrieved": "2026-08-31",
    "base": 15960,
    "increment": 5680,
    "published_table": {
        1: 15960,
        2: 21640,
        3: 27320,
        4: 33000,
        5: 38680,
        6: 44360,
        7: 50040,
        8: 55720,
    },
}




def poverty_line(household_size):
    if household_size < 1:
        raise ValueError(f"Household size must be at least 1, got {household_size}")
    base = POVERTY_GUIDELINES_2026["base"]
    increment = POVERTY_GUIDELINES_2026["increment"]
    return base + increment * (household_size - 1)





    
def fpl_percentage(annual_income, household_size):
    if household_size < 1:
        raise ValueError(f"Household size must be at least 1, got {household_size}")
    if annual_income < 0:
        raise ValueError(f"Annual income must be a non-negative number, got {annual_income}")
    return annual_income / poverty_line(household_size) * 100
    



def screen(household, programs=None):
    from screening.program_rules import PROGRAMS, check_rule

    if programs is None:
        selected_programs = PROGRAMS
    else:
        if isinstance(programs, str):
            programs = [programs]

        lookup = {program["id"]: program for program in PROGRAMS}
        selected_programs = []
        for program in programs:
            if isinstance(program, str):
                if program not in lookup:
                    raise ValueError(f"Unknown program id: {program}")
                selected_programs.append(lookup[program])
            else:
                selected_programs.append(program)

    results = []

    for program in selected_programs:
        qualifies = True
        explanations = []

        for rule in program["rules"]:
            passed, explanation = check_rule(rule, household)
            explanations.append(explanation)
            if not passed:
                qualifies = False

        results.append({
            "program_id": program["id"],
            "name": program["name"],
            "qualifies": qualifies,
            "explanations": explanations,
            "apply_url": program["apply_url"],
        })

    return results
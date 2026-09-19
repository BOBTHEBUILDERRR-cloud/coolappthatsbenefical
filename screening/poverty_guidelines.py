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
    base = POVERTY_GUIDELINES_2026["base"]
    increment = POVERTY_GUIDELINES_2026["increment"]
    return base + increment * (household_size - 1)




    
def fpl_percentage(annual_income, household_size):
    return annual_income / poverty_line(household_size) * 100
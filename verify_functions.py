from screening.poverty_guidelines import POVERTY_GUIDELINES_2026, poverty_line, fpl_percentage, screen
from screening.county_search import county_for_zip

from screening.program_rules import PROGRAMS, check_rule

required_fields = ["id", "name", "agency", "apply_url", "source_url",
                   "retrieved", "rules", "benefit_value", "documents"]

for program in PROGRAMS:
    for field in required_fields:
        assert field in program, f"{program['id']} is missing {field}"

def find(results, program_id):
    for result in results:
        if result["program_id"] == program_id:
            return result
    raise ValueError(f"No result for {program_id}")


assert county_for_zip("95112") == "Santa Clara"
assert county_for_zip("not a zip") is None
for size, published in POVERTY_GUIDELINES_2026["published_table"].items():
    computed = poverty_line(size)
    assert computed == published, (
        f"Household of {size}: formula gives {computed}, HHS published {published}"
    )
assert fpl_percentage(33000,4) == 100.0
assert fpl_percentage(16500,4) == 50.0
assert poverty_line(1) == 15960
assert poverty_line(2) == 21640
assert poverty_line(9) == 61400
assert fpl_percentage(0, 4) == 0.0

try:
    poverty_line(0)
    raise AssertionError("poverty_line(0) should have raised ValueError")
except ValueError:
    pass
try:
    fpl_percentage(-1, 4)
    raise AssertionError("Negative income should have raised ValueError")
except ValueError:
    pass
try:
    fpl_percentage(1000, 0)
    raise AssertionError("Invalid household size should have raised ValueError")
except ValueError:
    pass
try:
    poverty_line(-3)
    raise AssertionError("poverty_line(-3) should have raised ValueError")
except ValueError:
    pass


working_family = {
    "size": 4,
    "annual_income": 48000,
    "state": "CA",
    "county": "Santa Clara",
    "ages": [37, 35, 12, 8],
}
higher_earners = {
    "size": 6,
    "annual_income": 145000,
    "state": "CA",
    "county": "San Mateo",
    "ages": [44, 41, 16, 13, 9, 70],
}
def find(results, program_id):
    """Pull one program's result out of the list."""
    for result in results:
        if result["program_id"] == program_id:
            return result
    raise ValueError(f"No result for {program_id}")

results = screen(
    working_family,
    programs=["calfresh", "medi_cal", "school_meals_free", "school_meals_reduced"],
)
assert find(results, "calfresh")["qualifies"] is True        
assert find(results, "medi_cal")["qualifies"] is False      
assert find(results, "school_meals_free")["qualifies"] is False
assert find(results, "school_meals_reduced")["qualifies"] is True
assert len(results) == 4
assert screen(working_family, programs="calfresh")[0]["program_id"] == "calfresh"
for result in screen(higher_earners):
    assert result["qualifies"] is False
exactly_at_limit = {
    "size": 4,
    "annual_income": 66000,         
    "state": "CA",
    "county": "Santa Clara",
    "ages": [40, 38, 10, 6],
}
assert find(screen(exactly_at_limit), "calfresh")["qualifies"] is True
one_dollar_over = dict(exactly_at_limit)
one_dollar_over["annual_income"] = 66001
assert find(screen(one_dollar_over), "calfresh")["qualifies"] is False

child_rule_result, child_rule_explanation = check_rule(
    {"type": "has_child_under", "value": 19}, working_family
)
assert child_rule_result is True
assert "under 19" in child_rule_explanation
residency_result, residency_explanation = check_rule(
    {"type": "state_residency", "value": "CA"}, working_family
)
assert residency_result is True
assert "residents of CA" in residency_explanation
nonresident_result, _ = check_rule(
    {"type": "state_residency", "value": "NY"}, working_family
)
assert nonresident_result is False

try:
    screen(working_family, programs=["not_a_program"])
    raise AssertionError("Unknown program should have raised ValueError")
except ValueError:
    pass


try:
    check_rule({"type": "not_a_real_rule", "value": 1}, working_family)
    raise AssertionError("Unknown rule type should have raised ValueError")
except ValueError:
    pass



results = screen(working_family)
assert find(results, "calfresh")["qualifies"] is True              # 145% under 200%
assert find(results, "medi_cal")["qualifies"] is False             # 145% over 138%
assert find(results, "school_meals_free")["qualifies"] is False    # 145% over 130%
assert find(results, "school_meals_reduced")["qualifies"] is True  # 145% under 185%

care_at_limit = {
    "size": 4,
    "annual_income": 66000,
    "state": "CA",
    "county": "Santa Clara",
    "ages": [37, 35, 12, 8],
}
care_over_limit = dict(care_at_limit)
care_over_limit["annual_income"] = 66001
care_below_limit = dict(care_at_limit)
care_below_limit["annual_income"] = 65000
assert find(screen(care_below_limit), "care")["qualifies"] is True
assert find(screen(care_at_limit), "care")["qualifies"] is True
assert find(screen(care_over_limit), "care")["qualifies"] is False
care_one_person = dict(care_at_limit)
care_one_person.update(size=1, annual_income=43280, ages=[37])
assert find(screen(care_one_person), "care")["qualifies"] is True
try:
    check_rule(
        PROGRAMS[-1]["rules"][0],
        {"size": 4, "annual_income": -1},
    )
    raise AssertionError("Negative CARE income should have raised ValueError")
except ValueError:
    pass
print("all checks passed.")
from screening.poverty_guidelines import POVERTY_GUIDELINES_2026, poverty_line, fpl_percentage

for size, published in POVERTY_GUIDELINES_2026["published_table"].items():
    computed = poverty_line(size)
    assert computed == published, (
        f"Household of {size}: formula gives {computed}, HHS published {published}"
    )
assert fpl_percentage(33000,4) == 100.0
print("All checks passed.")
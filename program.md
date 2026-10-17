# Adding a Program

Use this guide to add a program to the screener without turning a published
income limit into a guess. Keep the official source and its effective dates
with the data.

## 1. Finding the rules

Start with a plain-language page from the agency that runs the program. Search
for the program name, the agency, and the eligibility year (for example,
`California CARE 2026 income limits`). Use that page to understand the benefit,
application route, and eligibility options. Cite the agency's official program
or eligibility index page in `source_url`; prefer a maintained index page over
a PDF that may be replaced. If the plain-language page is not the official
source, keep it open while checking the matching official rule.

Record the agency, application URL, source URL, and the date you checked the
source. Do not treat a search result snippet as the rule. Follow links to the
agency page and verify the actual limits and effective dates there.

## 2. The four questions

Answer these from the official source before writing JSON:

- What income limit applies, and is it a percentage of FPL or a dollar amount
  that varies by household size?
- Does the source mean gross income (before taxes), net income, or something
  else? The screener's `annual_income` must use the same definition. If the
  source does not say, do not silently assume; record the ambiguity in the
  program's `notes` and seek clarification.
- Is exactly on the limit included? Terms such as "at or below" mean `<=`;
  preserve the source's actual boundary.
- What official URL supports the rule, and on what date did you check it?

Also note any non-income paths to eligibility, such as enrollment in another
program, residency, age, or utility service area. Do not replace those paths
with an income rule unless the source says they are optional.

## 3. Checking your numbers

The screener's `poverty_line(size)` is the 2026 HHS guideline for the 48
contiguous states and DC. Take the published dollar limit for a household of 4
and for a household of 1. Divide each by `poverty_line(size)` and multiply by
100. For a single FPL percentage, both should match the stated percentage,
subject only to documented rounding. For example, 200% of the 2026 guideline
is $66,000 for 4 people and $31,920 for 1 person.

For a size-based table, compare each amount with the published value and report
both implied percentages. They may differ because sizes are grouped or the
program uses a different formula. For example, CARE's $43,280 limit for a
1-person household is about 271% of the $15,960 guideline, while its $66,000
limit for 4 is 200% of $33,000; the source groups sizes 1-2 at one dollar
limit. Explain the difference and use a rule type that preserves the
published limits; never store a dollar amount as an FPL percentage.

## 4. Where sources live

Find the data file by checking `DATA_FILE` in `screening/program_rules.py`.
Add the record to the JSON file that constant points to. Keep `source_url` on
an agency-maintained index or eligibility page, not a PDF when an index exists.
Put the date checked in `retrieved` as `YYYY-MM-DD`. If limits have an
effective period, include it in `notes`; check whether the agency updates the
page annually and revisit the record when the period changes. Do not change
the poverty guideline year or its shared math to accommodate one program's
different period.

## 5. A blank program record

Add one object to the top-level `programs` array:

```json
{
  "id": "short_unique_snake_case_id",
  "name": "Public program name",
  "agency": "Agency that runs the program",
  "apply_url": "https://agency.example/apply",
  "source_url": "https://agency.example/eligibility",
  "retrieved": "YYYY-MM-DD",
  "rules": [
    {"type": "income_below_fpl_pct", "value": 200}
  ],
  "benefit_value": {
    "type": "describe_the_benefit",
    "value": 0
  },
  "documents": ["Application item or proof the applicant may need"],
  "notes": "Optional qualifications, effective dates, or unresolved caveats."
}
```

`id` must be unique and is used by the screener and tests. `name` is the
display name. `agency`, `apply_url`, `source_url`, and `retrieved` identify who
runs it, where to apply, the evidence for the rule, and when it was checked.
`rules` is a list of eligibility checks that must all pass. `benefit_value`
describes the estimated benefit using the closest existing convention; do not
invent a dollar estimate unsupported by a source. `documents` is a list of
application materials to prepare. `notes` is optional and holds qualifications,
effective dates, and limitations the current screener cannot evaluate.

## 6. Rule types that already exist

| Type | Meaning of `value` | Example |
| --- | --- | --- |
| `income_below_fpl_pct` | Maximum percentage of 2026 FPL; equality passes | `{"type":"income_below_fpl_pct","value":200}` |
| `income_below_annual_limit_by_size` | `limits_by_size` maps household-size strings to annual dollar limits; `additional_person_limit` extends the largest configured size; equality passes | `{"type":"income_below_annual_limit_by_size","value":{"limits_by_size":{"1":43280,"2":43280,"3":54640,"4":66000},"additional_person_limit":11360}}` |
| `income_between_annual_limits_by_size` | Inclusive lower and upper annual dollar limits by household size; `minimum_limits_by_size` and `maximum_limits_by_size` map size strings to limits; `additional_person_minimum_limit` and `additional_person_maximum_limit` extend the largest configured size | `{"type":"income_between_annual_limits_by_size","value":{"minimum_limits_by_size":{"1":43281,"2":43281,"3":54641,"4":66001},"maximum_limits_by_size":{"1":54100,"2":54100,"3":68300,"4":82500},"additional_person_minimum_limit":11360,"additional_person_maximum_limit":14200}}` |
| `has_child_under` | Maximum age, exclusive; at least one household member must be younger | `{"type":"has_child_under","value":19}` |
| `state_residency` | Required state abbreviation | `{"type":"state_residency","value":"CA"}` |

Rules are combined with AND: every rule in the program's `rules` list must
pass. Income is compared with `<=`. The current household input has
`annual_income`, `size`, `state`, `county`, and `ages`; it does not currently
identify gross versus net income or utility provider.

## 7. When you need a new rule type

Use a new type only when no existing type can express the source's rule without
changing its meaning. For example, a published dollar-limit table by household
size cannot always be represented by one FPL percentage.

1. Add the calculation to `check_rule` in `screening/program_rules.py`. Read
   only the rule and household fields needed for the decision.
2. Return `(passed, explanation)`, where `passed` is a boolean and
   `explanation` tells the applicant why the rule passed or failed.
3. Add focused checks in `verify_functions.py`: one qualifying household, one
   failing household, and one exactly at the limit. The exact-limit check must
   match the source's inclusive or exclusive boundary.
4. Run `python verify_functions.py` and fix failures caused by the rule before
   adding more programs with it.

Avoid a new rule if the existing rule can express the published policy
faithfully. Do not make a shared rule type program-specific by hiding a special
case in it.

## 8. Things we can't check yet

The screener currently evaluates only the rule types listed above. If a
program also depends on a utility provider, service territory, enrollment in
another program, or another unsupported condition, do not claim the screener
has checked it. Explain the condition and what the applicant must confirm in
that program's `notes`. Add a rule type and the three checks in section 7 only
when the household data needed to evaluate it is available and the behavior is
clear from an official source.

## 9. Before you commit

- [ ] The program has a unique `id` and every required field is present.
- [ ] The agency source and the date checked are filled in.
- [ ] The source's income definition, effective period, and exact-limit
      behavior are represented or clearly noted as unresolved.
- [ ] The stored value is a percentage only when the verified rule is an FPL
      percentage, not a dollar limit.
- [ ] `benefit_value` and `documents` are present and supported by evidence.
- [ ] Any unsupported eligibility conditions are stated in `notes`.
- [ ] New rule types have pass, fail, and exact-limit checks.
- [ ] `python verify_functions.py` passes.
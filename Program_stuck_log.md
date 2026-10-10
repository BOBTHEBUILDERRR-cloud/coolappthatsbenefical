# Adding a Program: Stuck Log

- Requested `Data/programs.json`, but the loader points to `Data/benefit_programs.json` and the requested file does not exist; I checked `DATA_FILE` and will make `Data/programs.json` the loaded source.
- CARE's CPUC chart gives a grouped dollar limit for households 1-2, so one FPL percentage cannot preserve it for both sizes; I compared the chart with `poverty_line()` and will add a size-based limit rule.
- The CPUC page gives annual household limits but does not establish gross versus net in the material checked; I will preserve this uncertainty in CARE's `notes` rather than assume.
- The CPUC page qualifies the electric discount by utility size (smaller utilities offer 20%); the guide's generic benefit field did not say how to record variable rates, so I added the distinct value and its condition to `benefit_value` and `notes`.
- The new size-based rule was missing from the guide's rule table, and the first number-check instructions skipped calculating implied FPL percentages for tabular limits; I documented the rule and added explicit 1-person/4-person comparison steps.
- Pylance found the existing FPL branch called `fpl_percentage` without importing it; I added the missing import while integrating CARE, then will confirm with the verifier.
- After repairing imports, the verifier requested stale ID `school_meals` although the data has `school_meals_free` and `school_meals_reduced`; I aligned its targeted checks with the two records already asserted later in the file.
- The requested `python verify_functions.py` command is unavailable in this shell; `python3` is installed, and its baseline run exposed a wrong `check_rule` import plus a stray token in `program_rules.py` that must be fixed for the verifier to run.
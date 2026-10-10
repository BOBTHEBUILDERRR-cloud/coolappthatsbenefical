import csv
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent/"Data"/"zip_to_county_california.csv"
ZIP_TO_COUNTY = {}
with open(DATA_FILE) as f:
    reader = csv.DictReader(f)
    for row in reader:
        ZIP_TO_COUNTY[row["zip"]] = row["county"]
print(f"zip_to_county_california.csv loaded with {len(ZIP_TO_COUNTY)} ZIP codes.")
print(ZIP_TO_COUNTY)
def county_for_zip(zip_code):
    """Return the county for a ZIP code, or None if we don't cover it."""
    return ZIP_TO_COUNTY.get(zip_code)

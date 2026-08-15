import os
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "clean"
CLEAN.mkdir(parents=True, exist_ok=True)

def clean_data():
    regions = pd.read_csv(RAW / "regions.csv")
    events = pd.read_csv(RAW / "disaster_events.csv")
    impacts = pd.read_csv(RAW / "impact_assessment.csv")

    # 1. Deduplication using business keys
    regions = regions.drop_duplicates(subset=["region_id"], keep="first").copy()
    events = events.drop_duplicates(subset=["event_id"], keep="first").copy()
    impacts = impacts.drop_duplicates(subset=["impact_id"], keep="first").copy()

    # 2. Missing disaster type -> Unknown
    events["disaster_type"] = events["disaster_type"].fillna("Unknown")

    # 3. Invalid dates -> NaT (safe conversion)
    events["event_date"] = pd.to_datetime(events["event_date"], errors="coerce")

    # 4. Missing population -> median
    regions["population"] = pd.to_numeric(regions["population"], errors="coerce")
    population_median = regions["population"].median()
    regions["population"] = regions["population"].fillna(population_median)

    # 5. Missing affected people/losses -> 0
    impacts["affected_people"] = pd.to_numeric(
        impacts["affected_people"], errors="coerce"
    ).fillna(0)
    impacts["economic_loss_musd"] = pd.to_numeric(
        impacts["economic_loss_musd"], errors="coerce"
    ).fillna(0)

    # Consistent numeric types
    regions["region_id"] = regions["region_id"].astype(int)
    events["event_id"] = events["event_id"].astype(int)
    impacts["impact_id"] = impacts["impact_id"].astype(int)
    impacts["event_id"] = impacts["event_id"].astype(int)
    impacts["affected_people"] = impacts["affected_people"].astype(int)

    # Save clean tables
    regions.to_csv(CLEAN / "regions_clean.csv", index=False)
    events.to_csv(CLEAN / "disaster_events_clean.csv", index=False, date_format="%Y-%m-%d")
    impacts.to_csv(CLEAN / "impact_assessment_clean.csv", index=False)

    # Analytical dataset: event + impact only.
    # We intentionally do not join to regions on region name because the supplied
    # regions file contains multiple region_id rows for each state/region name.
    fact = events.merge(
        impacts[["event_id", "affected_people", "economic_loss_musd"]],
        on="event_id",
        how="left",
    )
    fact["affected_people"] = fact["affected_people"].fillna(0)
    fact["economic_loss_musd"] = fact["economic_loss_musd"].fillna(0)
    fact.to_csv(CLEAN / "disaster_fact_clean.csv", index=False)

    # Region-level population summary for reference
    region_summary = (
        regions.groupby("region", as_index=False)
        .agg(
            population=("population", "median"),
            area_sq_km=("area_sq_km", "median"),
            region_records=("region_id", "count"),
        )
    )
    region_summary.to_csv(CLEAN / "region_summary_clean.csv", index=False)

    print("ETL completed.")
    print(f"Regions: {len(regions)}")
    print(f"Events: {len(events)}")
    print(f"Impact rows: {len(impacts)}")
    print(f"Population median used: {population_median:,.0f}")
    print(f"Clean files written to: {CLEAN}")

if __name__ == "__main__":
    clean_data()

# Disaster-Affected Region Tracker Analysis

A Python, Pandas, and MySQL data-engineering/analytics project for cleaning disaster datasets, loading structured data into a relational database, and producing analytical visualizations.

## Overview

The project implements a complete local workflow:

```text
Raw CSV Data
    ↓
Python / Pandas ETL
    ↓
Cleaned Tables
    ↓
MySQL
    ↓
SQL Analytics
    ↓
Matplotlib Visualizations
```

## Data processing

The ETL workflow:
- Removes duplicates using business keys.
- Handles missing disaster types with `Unknown`.
- Converts invalid dates safely to null values.
- Fills missing population values using the population median.
- Treats missing affected-people and economic-loss values as zero.
- Produces cleaned tables and an event/impact analytical dataset.

## Database

Clean datasets can be loaded into MySQL with the included loader.

Main tables:
- `regions_clean`
- `disaster_events_clean`
- `impact_assessment_clean`

SQL analysis is provided in:

`sql/analysis_queries.sql`

## Analytics

The project generates five analytical charts:

1. Top 5 regions by total affected population
2. Disaster severity distribution by disaster type
3. Monthly disaster trend
4. Economic loss vs. affected population
5. Region-wise disaster frequency heatmap

## Project structure

```text
Disaster-Affected-Region-Tracker-Analysis/
├── data/
│   ├── raw/
│   └── clean/
├── output/
├── sql/
│   ├── schema.sql
│   └── analysis_queries.sql
├── src/
│   ├── etl.py
│   ├── load_mysql.py
│   └── dashboard.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Run locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the ETL:

```bash
python src/etl.py
```

Generate visualizations:

```bash
python src/dashboard.py
```

Configure MySQL credentials in `.env` and load the cleaned tables:

```bash
python src/load_mysql.py
```

## Data-model note

The supplied region dataset contains multiple records for the same region name. The analytical fact dataset therefore joins disaster events to impact data by `event_id` and does not join events to the region table by region name, avoiding duplicate analytical rows.

## Scope limitation

The supplied datasets contain region names and disaster-related attributes but no latitude/longitude, GIS geometries, satellite imagery, or remote-sensing bands. The current implementation therefore provides region-level analysis rather than geographic mapping.

## Technology

**Python · Pandas · NumPy · MySQL · SQL · Matplotlib**

## Author

Harsha Vinay Garagaparthi

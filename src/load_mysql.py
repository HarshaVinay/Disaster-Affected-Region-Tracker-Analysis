import os
from pathlib import Path

import pandas as pd
import mysql.connector
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "clean"

# Load .env from the project root
load_dotenv(ROOT / ".env")

DB_NAME = os.getenv("MYSQL_DATABASE", "disaster_tracker")


def get_connection(database=None):
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=database,
    )


def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`"
    )

    cursor.close()
    conn.close()


def convert_nan_to_none(value):
    """
    Convert Pandas/NumPy missing values to Python None.

    MySQL Connector converts Python None to SQL NULL.
    """
    if pd.isna(value):
        return None

    return value


def load_tables():

    # -------------------------------------------------
    # 1. Create database
    # -------------------------------------------------

    create_database()

    # -------------------------------------------------
    # 2. Connect to database
    # -------------------------------------------------

    conn = get_connection(DB_NAME)
    cursor = conn.cursor()

    # -------------------------------------------------
    # 3. Create tables
    # -------------------------------------------------

    schema = (ROOT / "sql" / "schema.sql").read_text(
        encoding="utf-8"
    )

    statements = [
        statement.strip()
        for statement in schema.split(";")
        if statement.strip()
    ]

    for statement in statements:
        cursor.execute(statement)

    # -------------------------------------------------
    # 4. Define tables and columns
    # -------------------------------------------------

    tables = {

        "regions_clean": [
            "region_id",
            "region",
            "population",
            "area_sq_km"
        ],

        "disaster_events_clean": [
            "event_id",
            "disaster_type",
            "region",
            "event_date",
            "severity"
        ],

        "impact_assessment_clean": [
            "impact_id",
            "event_id",
            "affected_people",
            "economic_loss_musd"
        ]
    }

    # -------------------------------------------------
    # 5. Load each table
    # -------------------------------------------------

    for table, columns in tables.items():

        file_path = CLEAN / f"{table}.csv"

        print(f"\nLoading {file_path.name}...")

        df = pd.read_csv(file_path)

        # Convert every NaN / NaT to Python None
        df = df.astype(object).where(
            pd.notna(df),
            None
        )

        placeholders = ",".join(
            ["%s"] * len(columns)
        )

        column_names = ",".join(columns)

        sql = f"""
            INSERT INTO {table}
            ({column_names})
            VALUES ({placeholders})
        """

        values = []

        for _, row in df.iterrows():

            row_values = tuple(
                convert_nan_to_none(row[column])
                for column in columns
            )

            values.append(row_values)

        cursor.executemany(sql, values)

        print(
            f"Inserted {len(values)} rows into {table}"
        )

    # -------------------------------------------------
    # 6. Commit
    # -------------------------------------------------

    conn.commit()

    cursor.close()
    conn.close()

    print("\n----------------------------------------")
    print(f"MySQL database `{DB_NAME}` loaded successfully.")
    print("----------------------------------------")


if __name__ == "__main__":
    load_tables()
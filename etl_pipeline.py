import pandas as pd
import sqlite3
from pathlib import Path
# --------------------------------------------------

# NHS Provider Financial Performance Dashboard

# ETL / Database Loading Pipeline

# --------------------------------------------------

# Project folders

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_DIR / "data"

# Input file

INPUT_FILE = DATA_DIR / "nhs_cleaned_data_2024_25.xlsx"

# SQLite database

DATABASE_FILE = PROJECT_DIR / "nhs_financials.db"

# --------------------------------------------------

# 1. Extract

# --------------------------------------------------

print("Reading NHS cleaned data...")

summary_df = pd.read_excel(

    INPUT_FILE,

    sheet_name="Summary by Trust"

)

detail_df = pd.read_excel(

    INPUT_FILE,

    sheet_name="Income Statement Detail"

)

print(f"Summary records: {len(summary_df):,}")

print(f"Detail records: {len(detail_df):,}")

# --------------------------------------------------

# 2. Transform

# --------------------------------------------------

print("Cleaning column names...")

summary_df.columns = [

    column.strip()

    for column in summary_df.columns

]

detail_df.columns = [

    column.strip()

    for column in detail_df.columns

]

# Remove completely empty rows

summary_df = summary_df.dropna(how="all")

detail_df = detail_df.dropna(how="all")

# Make NHS codes text

summary_df["NHS Code"] = summary_df["NHS Code"].astype(str).str.strip()

detail_df["NHS Code"] = detail_df["NHS Code"].astype(str).str.strip()

print("Transformation complete.")

# --------------------------------------------------

# 3. Load into SQLite

# --------------------------------------------------

print("Creating SQLite database...")

connection = sqlite3.connect(DATABASE_FILE)

summary_df.to_sql(

    "summary_by_trust",

    connection,

    if_exists="replace",

    index=False

)

detail_df.to_sql(

    "income_statement_detail",

    connection,

    if_exists="replace",

    index=False

)

# --------------------------------------------------

# 4. Validation

# --------------------------------------------------

summary_count = pd.read_sql_query(

    "SELECT COUNT(*) AS count FROM summary_by_trust",

    connection

)["count"].iloc[0]

detail_count = pd.read_sql_query(

    "SELECT COUNT(*) AS count FROM income_statement_detail",

    connection

)["count"].iloc[0]

print()

print("ETL pipeline completed successfully.")

print("------------------------------------")

print(f"Summary records loaded: {summary_count:,}")

print(f"Detail records loaded:  {detail_count:,}")

print(f"Database created: {DATABASE_FILE}")

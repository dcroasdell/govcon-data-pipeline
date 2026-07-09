import duckdb
import json

# Load the raw JSON we just saved
with open("/usr/local/airflow/include/data/dod_awards_2024.json", "r") as f:
    records = json.load(f)

print(f"Loaded {len(records)} records from file")

# Connect to (or create) a local DuckDB database file
con = duckdb.connect("/usr/local/airflow/include/data/govcon.duckdb")

# DuckDB can read a list of JSON-like dicts directly via pandas
import pandas as pd
df = pd.DataFrame(records)

print(df.head())
print(f"\nColumns: {list(df.columns)}")

# Create a raw table from this dataframe
con.execute("CREATE OR REPLACE TABLE raw_awards AS SELECT * FROM df")

# Quick sanity check
result = con.execute("SELECT COUNT(*) FROM raw_awards").fetchone()
print(f"\nRows loaded into raw_awards table: {result[0]}")

con.close()
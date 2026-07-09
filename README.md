GovCon Contract & Spending Analytics Pipeline

A full-stack data engineering pipeline that extracts federal contract award data from USAspending.gov, models it into a dimensional (star) schema using dbt, orchestrates the workflow with Apache Airflow, and serves insights through Power BI.

Built as a hands-on portfolio project to demonstrate the modern data stack (Python → DuckDB → dbt → Airflow → BI) applied to a real-world GovCon (government contracting) domain.


Architecture

USAspending.gov API
        │
        ▼
  Python Extraction (requests)
        │
        ▼
   DuckDB (local warehouse)
        │
        ▼
   dbt (staging → star schema)
        │
        ▼
  Apache Airflow (orchestration)
        │
        ▼
   Power BI (dashboard)

Star schema:


fact_awards — one row per contract award, with FKs to each dimension
dim_vendors — unique contract recipients
dim_agencies — awarding agency / sub-agency hierarchy
dim_time — date dimension (year, quarter, month) derived from award start/end dates



Tech Stack

LayerToolExtractionPython (requests)WarehouseDuckDBTransformationdbt Core (dbt-duckdb)OrchestrationApache Airflow (via Astronomer's Astro CLI + Docker)VisualizationPower BIData SourceUSAspending.gov API — free, public, no auth required


Project Structure

govcon-data-pipeline/
├── src/extract/              # Standalone Python extraction & load scripts
│   ├── explore_api.py        # Pulls award data from USAspending API
│   └── load_to_duckdb.py     # Loads raw JSON into DuckDB
├── govcon_dbt/                # dbt project (local dev)
│   └── models/
│       ├── staging/           # stg_awards.sql — cleaned column names/types
│       └── marts/             # dim_vendors, dim_agencies, dim_time, fact_awards
├── airflow_project/           # Astro/Airflow project
│   ├── dags/
│   │   └── govcon_pipeline.py # DAG: extract → load → dbt run → dbt test
│   └── include/               # Copies of src/ and govcon_dbt/ used inside containers
├── requirements.txt
└── README.md


Pipeline Steps


Extract — explore_api.py calls the USAspending spending_by_award endpoint, paginating through Department of Defense contract awards for a given time period, and saves the results as raw JSON.
Load — load_to_duckdb.py reads the raw JSON and loads it into a raw_awards table in a local DuckDB file.
Transform — dbt builds a staging model (stg_awards) to clean and rename columns, then builds the dimensional model:

dim_vendors, dim_agencies, dim_time — deduplicated dimension tables with surrogate keys
fact_awards — the fact table, joining stg_awards against each dimension



Test — dbt test validates the models (not-null / uniqueness checks).
Orchestrate — an Airflow DAG (govcon_pipeline) runs the full sequence end-to-end on a schedule, using BashOperator tasks for each step.
Serve — Power BI connects to the DuckDB warehouse to visualize spending trends by agency, vendor, and time period.



Running Locally

Prerequisites: Python 3.12, Docker Desktop, Git

bash# Clone the repo
git clone https://github.com/dcroasdell/govcon-data-pipeline.git
cd govcon-data-pipeline

# Set up the Python environment
python -m venv venv
venv\Scripts\activate      # Windows
pip install -r requirements.txt

# Run extraction + load manually
python src/extract/explore_api.py
python src/extract/load_to_duckdb.py

# Run dbt transformations
cd govcon_dbt
dbt run
dbt test

Run the full pipeline via Airflow:

bashcd airflow_project
astro dev start

Then open the Airflow UI at http://localhost:8080 (default login admin / admin), and trigger the govcon_pipeline DAG.


Notes & Known Limitations


NAICS codes are largely unavailable through the spending_by_award search endpoint and are left as a future enhancement (would require per-award detail calls to a different endpoint).
This project runs Airflow locally via Docker for development/demo purposes. A production deployment would use a managed Airflow service (e.g. Astronomer Cloud, AWS MWAA) or a persistent cloud VM rather than a local machine.
Data is currently scoped to Department of Defense awards for a single fiscal year as a proof of concept; the extraction script can be parameterized to pull additional agencies or time periods.

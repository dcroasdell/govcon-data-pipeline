## Connecting Power BI
This repo includes `govcon.pbix`, pre-built against the author's local DuckDB path. 
To use it yourself:
1. Run the pipeline steps above to generate `data/govcon.duckdb`
2. Install the DuckDB ODBC driver + Power Query connector (see links in README)
3. In Power BI: Transform Data → Data Source Settings → update the file path to match your local `data/govcon.duckdb` location
4. Refresh



Initial View
Please look at govcon.png for image of the dashboard given fields brought into the project. 

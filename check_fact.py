import duckdb

con = duckdb.connect('data/govcon.duckdb')

# Overall row count
total = con.execute('SELECT COUNT(*) FROM fact_awards').fetchone()
print(f"Total fact rows: {total[0]}")

# Check for broken joins (nulls where they shouldn't be)
nulls = con.execute('''
    SELECT
        SUM(CASE WHEN vendor_id IS NULL THEN 1 ELSE 0 END) as missing_vendor,
        SUM(CASE WHEN agency_id IS NULL THEN 1 ELSE 0 END) as missing_agency,
        SUM(CASE WHEN start_time_id IS NULL THEN 1 ELSE 0 END) as missing_time
    FROM fact_awards
''').fetchdf()
print("\nMissing foreign keys:")
print(nulls)

# Sample joined output - proving the star schema actually works together
sample = con.execute('''
    SELECT
        v.recipient_name,
        ag.awarding_sub_agency,
        t.year,
        f.award_amount
    FROM fact_awards f
    JOIN dim_vendors v ON f.vendor_id = v.vendor_id
    JOIN dim_agencies ag ON f.agency_id = ag.agency_id
    JOIN dim_time t ON f.start_time_id = t.time_id
    ORDER BY f.award_amount DESC
    LIMIT 5
''').fetchdf()
print("\nTop 5 awards (fully joined across the star schema):")
print(sample)

con.close()
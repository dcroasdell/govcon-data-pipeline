import duckdb

con = duckdb.connect('data/govcon.duckdb')

result = con.execute('''
    SELECT * FROM dim_agencies
    ORDER BY agency_id
''').fetchdf()

print(result)

total = con.execute('SELECT COUNT(*) FROM dim_agencies').fetchone()
print(f"\nTotal unique agency/sub-agency combos: {total[0]}")

con.close()
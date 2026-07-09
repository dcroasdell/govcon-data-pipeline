import duckdb

con = duckdb.connect('data/govcon.duckdb')

result = con.execute('''
    SELECT * FROM dim_vendors
    ORDER BY vendor_id
    LIMIT 10
''').fetchdf()

print(result)

total = con.execute('SELECT COUNT(*) FROM dim_vendors').fetchone()
print(f"\nTotal unique vendors: {total[0]}")

con.close()
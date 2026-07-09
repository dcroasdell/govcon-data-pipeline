import duckdb

con = duckdb.connect('data/govcon.duckdb')

result = con.execute('''
    SELECT * FROM dim_time
    ORDER BY award_date
    LIMIT 10
''').fetchdf()

print(result)

total = con.execute('SELECT COUNT(*) FROM dim_time').fetchone()
print(f"\nTotal unique dates: {total[0]}")

con.close()
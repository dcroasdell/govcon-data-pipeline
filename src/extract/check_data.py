import duckdb

con = duckdb.connect('data/govcon.duckdb')

result = con.execute('''
    SELECT "Recipient Name", "Award Amount"
    FROM raw_awards
    ORDER BY "Award Amount" DESC
    LIMIT 5
''').fetchdf()

print(result)

con.close()
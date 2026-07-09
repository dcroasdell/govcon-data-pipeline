import duckdb

con = duckdb.connect('data/govcon.duckdb')

result = con.execute('''
    SELECT recipient_name, award_amount, awarding_agency, start_date
    FROM stg_awards
    ORDER BY award_amount DESC
    LIMIT 5
''').fetchdf()

print(result)

con.close()
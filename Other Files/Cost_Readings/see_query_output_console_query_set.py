import psycopg2

# Connect to postgres DB
conn = psycopg2.connect(dbname = "postgres", user = "postgres", password = '*****', port = '5432' )
#conn = psycopg2.connect(host= ‘localhost’, dbname = ‘postgres’, user = ‘postgres’, password = ‘’, port = 5432)

# Open a cursor to perform database operations
cur = conn.cursor()

# List of queries to run
queries = [
    """SELECT * FROM connecsens.json_montoldre_row LIMIT 5""",
    """SELECT COUNT(*) FROM connecsens.json_montoldre_row"""
]

for query in queries:
    cur.execute(query)
    results = cur.fetchall()
    for row in results:
        print(row)
# Close the cursor and connection
cur.close()
conn.close()

#for query in queries:
    #cur.execute(query)
    #result = cur.fetchone()
    #print(result)

# Commit the transaction (if any changes were made)
#conn.commit()
import psycopg2

# Connect to postgres DB
conn = psycopg2.connect(dbname="postgres", user="postgres", password='*****', port='5432')

# Open a cursor to perform database operations
cur = conn.cursor()

# List of queries to run
queries = [

    """SELECT attname AS column_name, n_distinct AS estimated_cardinality 
    FROM pg_stats WHERE schemaname = 'connecsens' AND 
    tablename = 'json_montoldre_row'"""
]
results = []

for query in queries:
    cur.execute(query)
    rows = cur.fetchall()
    for row in rows:
        column_name, estimated_cardinality = row
        results.append((column_name, estimated_cardinality))
        print(f"Column: {column_name}, Estimated Cardinality: {estimated_cardinality}")
        
# Close communication with the database
cur.close()
conn.close()
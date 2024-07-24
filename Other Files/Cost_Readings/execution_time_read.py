import psycopg2

queries = [
    """SELECT * FROM connecsens.json_montoldre_row LIMIT 5""",
    """SELECT COUNT(*) FROM connecsens.json_montoldre_row"""
]

# Connect to PostgreSQL
conn = psycopg2.connect(dbname="postgres", user="postgres", password='manvim', port='5432')
cursor = conn.cursor()

# Loop through each query
for query in queries:
    # Execute EXPLAIN ANALYZE for the query
    cursor.execute("EXPLAIN ANALYZE " + query)
    # Fetch and print the execution plan
    rows = cursor.fetchall()
    for row in rows:
        if "Execution Time:" in row[0]:
            execution_time = row[0].split(":")[1].strip()
            print("Execution Time:", execution_time)

# Close the cursor and connection
if cursor:
    cursor.close()
if conn:
    conn.close()

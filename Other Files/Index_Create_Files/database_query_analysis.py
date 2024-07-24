import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(dbname="postgres", user="postgres", password='manvim', port='5432')
cursor = conn.cursor()

# Define the query to get the top 5 statements
query = """
SELECT query, calls 
FROM pg_stat_statements
WHERE (query LIKE 'SELECT%' OR 
       query LIKE 'EXPLAIN%' OR 
       query LIKE 'INSERT%' OR 
       query LIKE 'DELETE%') 
  AND calls > 5
ORDER BY calls DESC
LIMIT 5;
"""

# Execute the query
cursor.execute(query)
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(f"Query: {row[0]}, Calls: {row[1]}")

# Close the cursor and connection
if cursor:
    cursor.close()
if conn:
    conn.close()

import psycopg2

queries = [

         """SELECT * FROM connecsens.json_montoldre_row LIMIT 5000""",

        """SELECT COUNT(*) FROM connecsens.json_montoldre_row"""
]

# Connect to PostgreSQL
conn = psycopg2.connect(dbname="postgres", user="postgres", password='*****', port='5432')
cursor = conn.cursor()

total_execution_time = 0
num_queries = len(queries)

# Loop through each query
for i, query in enumerate(queries):
    query_number = f"Q{i+1}"

    # Execute EXPLAIN ANALYZE for the query
    cursor.execute("EXPLAIN ANALYZE " + query)

    # Fetch and print the execution plan
    rows = cursor.fetchall()

    for row in rows:
        if "Execution Time:" in row[0]:
            execution_time_str = row[0].split(":")[1].strip().split(" ")[0]
            execution_time = float(execution_time_str)
            
            total_execution_time += execution_time
            print(f"Execution Time for query '{query_number}': {execution_time} ms")

average_execution_time = total_execution_time / num_queries

print(f"Total Execution Time: {total_execution_time} ms")
print(f"Average Execution Time: {average_execution_time} ms")

# Close the cursor and connection
if cursor:
    cursor.close()
if conn:
    conn.close()

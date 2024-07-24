import psycopg2
import re
import csv

def read_queries_from_file(file_path):
    with open(file_path, 'r') as file:
        queries = file.read()

        # Remove comments
        queries = re.sub(r'--.*', '', queries)

        # Assuming each query in the file is separated by a semicolon
        queries = queries.split(';')
        queries = [query.strip() for query in queries if query.strip()]

        return queries

# Path to the SQL file
file_path = 'Workload7.sql'

# Read queries from the SQL file
queries = read_queries_from_file(file_path)

# Connect to PostgreSQL
conn = psycopg2.connect(dbname="postgres", user="postgres", password='*****', port='5432')
cursor = conn.cursor()

total_execution_time = 0
num_queries = len(queries)

# Prepare CSV file for writing
csv_file_path = 'execution_times_WL7.csv'
csv_headers = ['Query Number', 'Execution Time (ms)']

with open(csv_file_path, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(csv_headers)

    # Loop through each query
    for i, query in enumerate(queries):
        query_number = f"Q{i+1}"

        # Execute EXPLAIN ANALYZE for the query
        cursor.execute("EXPLAIN ANALYZE " + query)

        # Fetch the execution plan
        rows = cursor.fetchall()

        for row in rows:
            if "Execution Time:" in row[0]:
                execution_time_str = row[0].split(":")[1].strip().split(" ")[0]
                execution_time = float(execution_time_str)
                
                total_execution_time += execution_time
                print(f"Execution Time for query '{query_number}': {execution_time} ms")
                
                # Write the result to the CSV file
                writer.writerow([query_number, execution_time])

# Calculate average execution time
average_execution_time = total_execution_time / num_queries

# Write total and average execution times to the CSV file
with open(csv_file_path, mode='a', newline='') as csv_file: # to the CSV file
    writer = csv.writer(csv_file)   # to the CSV file
    writer.writerow(['Total Execution Time', total_execution_time])   # to the CSV file
    writer.writerow(['Average Execution Time', average_execution_time])  # to the CSV file

print(f"Total Execution Time: {total_execution_time} ms")
print(f"Average Execution Time: {average_execution_time} ms")

# Close the cursor and connection
if cursor:
    cursor.close()
    
if conn:
    conn.close()

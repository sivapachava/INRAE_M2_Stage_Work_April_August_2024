import psycopg2
import csv

# Read queries from a .sql file
def read_queries_from_file(file_path):
    with open(file_path, 'r') as file:
        queries = file.read().split(';')
    return [query.strip() for query in queries if query.strip()]

# Specify the path to your SQL file
sql_file_path = "Workload7.sql"

# Get queries from the SQL file
queries = read_queries_from_file(sql_file_path)

# Connect to PostgreSQL
conn = psycopg2.connect(dbname="postgres", user="postgres", password='manvim', port='5432')
cursor = conn.cursor()

# Initialize variables to store total initial and final costs
total_initial_cost = 0.0
total_final_cost = 0.0

# Prepare CSV file for writing
csv_file_path = 'query_costs_WL7_BIndex_ind.csv'
csv_headers = ['Query Number', 'Operator', 'Initial Cost', 'Final Cost']

with open(csv_file_path, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(csv_headers)

    # Loop through each query
    for i, query in enumerate(queries):
        query_number = f"Q{i+1}"

        # Execute EXPLAIN ANALYZE for the query
        cursor.execute("EXPLAIN ANALYZE " + query)

        # Fetch and print the execution plan
        rows = cursor.fetchall()

        for row in rows:
            if "cost=" in row[0]:    #i removed "and not row[0].startswith("Gather")"
                # Extract the operator name
                parts = row[0].split(' (cost=')
                operator = parts[0].strip()

                # Find and extract the cost part
                cost_index = row[0].find("cost=") + len("cost=")

                # Extracting the cost part
                costs = row[0][cost_index:].split(" ")[0]  

                # Splitting initial and final costs
                initial_cost, final_cost = costs.split("..") 

                # Convert costs to float and add to total
                total_initial_cost += float(initial_cost)
                total_final_cost += float(final_cost)

                # Print the result with query number and operator
                print(f"{query_number} {operator}: Initial Cost: {initial_cost} Final Cost: {final_cost}")

                # Write the result to the CSV file
                writer.writerow([query_number, operator, initial_cost, final_cost])

# Write total costs to the CSV file
with open(csv_file_path, mode='a', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Total Initial Cost', total_initial_cost])
    writer.writerow(['Total Final Cost', total_final_cost])

# Print the total initial and final costs
print(f"Total Initial Cost: {total_initial_cost:.2f}")
print(f"Total Final Cost: {total_final_cost:.2f}")

# Close the cursor and connection
if cursor:
    cursor.close()
if conn:
    conn.close()

import psycopg2
import csv

# Function to read queries from a .sql file
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

# Initialize dictionaries to store individual query costs
initial_costs = {}
final_costs = {}

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

        # Fetch the execution plan
        rows = cursor.fetchall()

        # Initialize variables to store query-specific costs
        total_initial_cost_query = 0.0
        total_final_cost_query = 0.0

        for row in rows:
            if "cost=" in row[0]:
                # Extract the operator name
                parts = row[0].split(' (cost=')
                operator = parts[0].strip()

                # Find and extract the cost part
                cost_index = row[0].find("cost=") + len("cost=")

                # Extracting the cost part
                costs = row[0][cost_index:].split(" ")[0]

                # Splitting initial and final costs
                initial_cost, final_cost = costs.split("..")

                # Convert costs to float and add to total for this query
                total_initial_cost_query += float(initial_cost)
                total_final_cost_query += float(final_cost)

                total_initial_cost += float(initial_cost)
                total_final_cost += float(final_cost)

                # Print the result with query number and operator
                print(f"{query_number} {operator}: Initial Cost: {initial_cost} Final Cost: {final_cost}")

                # Write the result to the CSV file
                writer.writerow([query_number, operator, initial_cost, final_cost])

        # Store total costs for this query in dictionaries
        initial_costs[query_number] = total_initial_cost_query
        final_costs[query_number] = total_final_cost_query

    # Write total costs for each query to the CSV file
    for query_number in initial_costs:
        writer.writerow([f"Total Initial Cost {query_number}", initial_costs[query_number]])
        writer.writerow([f"Total Final Cost {query_number}", final_costs[query_number]])

    # Write overall total costs to the CSV file
    writer.writerow(['Overall Total Initial Cost', total_initial_cost])
    writer.writerow(['Overall Total Final Cost', total_final_cost])

    # Print the total initial and final costs for each query
    print("\nIndividual Query Costs:")
    for query_number in initial_costs:
        print(f"{query_number}: Total Initial Cost: {initial_costs[query_number]:.2f}, Total Final Cost: {final_costs[query_number]:.2f}")

    # Print the overall total initial and final costs
    print("\nOverall Costs:")
    print(f"Total Initial Cost: {total_initial_cost:.2f}")
    print(f"Total Final Cost: {total_final_cost:.2f}")

# Close the cursor and connection
if cursor:
    cursor.close()
if conn:
    conn.close()
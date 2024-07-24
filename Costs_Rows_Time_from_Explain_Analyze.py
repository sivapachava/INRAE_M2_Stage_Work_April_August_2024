import psycopg2
import re
import csv

# Function to read queries from a .sql file
def read_queries_from_file(file_path):
    with open(file_path, 'r') as file:
        queries = file.read()

        # Remove comments
        queries = re.sub(r'--.*', '', queries)

        # Assuming each query in the file is separated by a semicolon
        queries = queries.split(';')
        queries = [query.strip() for query in queries if query.strip()]

        return queries

# Specify the path to your SQL file
file_path = 'Workload2.sql'

# Get queries from the SQL file
queries = read_queries_from_file(file_path)

# Connect to PostgreSQL
conn = psycopg2.connect(dbname="cebanewdata", user="postgres", password='manvim', port='5432')
cursor = conn.cursor()

# Prepare CSV files for writing
execution_csv_file_path = 'exe_times_WL2_AIndex_4GBfloat.csv'
costs_csv_file_path = 'query_costs_WL2_AIndex_4GBfloat.csv'
rows_csv_file_path = 'query_rows_WL2_AIndex_4GBfloat.csv'

execution_csv_headers = ['Query Number', 'Execution Time (ms)']
costs_csv_headers = ['Query Number', 'Operator', 'Initial Cost', 'Final Cost']
rows_csv_headers = ['Query Number', 'Operator', 'Planned Rows', 'Actual Rows']

with open(execution_csv_file_path, mode='w', newline='') as exec_csv_file, \
     open(costs_csv_file_path, mode='w', newline='') as cost_csv_file, \
     open(rows_csv_file_path, mode='w', newline='') as row_csv_file:

    exec_writer = csv.writer(exec_csv_file)
    cost_writer = csv.writer(cost_csv_file)
    row_writer = csv.writer(row_csv_file)

    exec_writer.writerow(execution_csv_headers)
    cost_writer.writerow(costs_csv_headers)
    row_writer.writerow(rows_csv_headers)

    total_execution_time = 0
    total_initial_cost = 0.0
    total_final_cost = 0.0
    total_planned_rows = 0
    total_actual_rows = 0

    initial_costs = {}
    final_costs = {}

    for i, query in enumerate(queries):
        query_number = f"Q{i+1}"

        # Execute EXPLAIN ANALYZE for the query
        cursor.execute("EXPLAIN ANALYZE " + query)

        # Fetch the execution plan
        rows = cursor.fetchall()

        total_initial_cost_query = 0.0
        total_final_cost_query = 0.0
        query_total_planned_rows = 0
        query_total_actual_rows = 0

        for row in rows:
            if "Execution Time:" in row[0]:
                execution_time_str = row[0].split(":")[1].strip().split(" ")[0]
                execution_time = float(execution_time_str)
                exec_writer.writerow([query_number, execution_time])
                print(f"Execution Time for query '{query_number}': {execution_time} ms")

            if "cost=" in row[0]:
                parts = row[0].split(' (cost=')
                operator = parts[0].strip()
                cost_index = row[0].find("cost=") + len("cost=")
                costs = row[0][cost_index:].split(" ")[0]
                initial_cost, final_cost = costs.split("..")
                initial_cost = float(initial_cost)
                final_cost = float(final_cost)

                total_initial_cost_query += initial_cost
                total_final_cost_query += final_cost
                total_initial_cost += initial_cost
                total_final_cost += final_cost

                cost_writer.writerow([query_number, operator, initial_cost, final_cost])
                print(f"{query_number} {operator}: Initial Cost: {initial_cost} Final Cost: {final_cost}")

            if "rows=" in row[0]:
                parts = row[0].split(' (cost=')
                operator = parts[0].strip()
                rows_index = row[0].find("rows=") + len("rows=")
                rows_part = row[0][rows_index:].split(" ")[0]
                planned_rows = int(rows_part.split()[0])

                actual_rows_index = row[0].find("rows=", rows_index) + len("rows=")
                actual_rows_part = row[0][actual_rows_index:].strip().split(" ")[0]

                try:
                    actual_rows = int(actual_rows_part)
                except ValueError:
                    actual_rows = 0

                query_total_planned_rows += planned_rows
                query_total_actual_rows += actual_rows

                row_writer.writerow([query_number, operator, planned_rows, actual_rows])
                print(f"{query_number} {operator}: Planned Rows: {planned_rows} Actual Rows: {actual_rows}")

        initial_costs[query_number] = total_initial_cost_query
        final_costs[query_number] = total_final_cost_query

        row_writer.writerow([query_number, 'Total', query_total_planned_rows, query_total_actual_rows])
        total_planned_rows += query_total_planned_rows
        total_actual_rows += query_total_actual_rows


        total_execution_time += execution_time
        average_execution_time = total_execution_time / len(queries)
    
    with open(execution_csv_file_path, mode='a', newline='') as exec_csv_file:
        exec_writer = csv.writer(exec_csv_file)
        exec_writer.writerow(['Total Execution Time', total_execution_time])
        exec_writer.writerow(['Average Execution Time', average_execution_time])
    
    for query_number in initial_costs:
        cost_writer.writerow([f"Total Initial Cost {query_number}", initial_costs[query_number]])
        cost_writer.writerow([f"Total Final Cost {query_number}", final_costs[query_number]])

        #row_writer.writerow([query_number, 'Total Planned Rows', query_total_planned_rows])
        #row_writer.writerow([query_number, 'Total Actual Rows', query_total_actual_rows])

    cost_writer.writerow(['Overall Total Initial Cost', total_initial_cost])
    cost_writer.writerow(['Overall Total Final Cost', total_final_cost])
    
    row_writer.writerow(['Overall Total Planned Rows', total_planned_rows])
    row_writer.writerow(['Overall Total Actual Rows', total_actual_rows])

print(f"Total Execution Time: {total_execution_time} ms")
print(f"Average Execution Time: {average_execution_time} ms")
print("\nIndividual Query Costs:")
for query_number in initial_costs:
    print(f"{query_number}: Total Initial Cost: {initial_costs[query_number]:.2f}, Total Final Cost: {final_costs[query_number]:.2f}")
print(f"\nOverall Costs:")
print(f"Total Initial Cost: {total_initial_cost:.2f}")
print(f"Total Final Cost: {total_final_cost:.2f}")
print(f"Overall Total Planned Rows: {total_planned_rows}")
print(f"Overall Total Actual Rows: {total_actual_rows}")

# Close the cursor and connection
if cursor:
    cursor.close()
if conn:
    conn.close()
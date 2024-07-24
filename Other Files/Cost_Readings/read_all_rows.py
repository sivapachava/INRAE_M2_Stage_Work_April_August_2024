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

# Initialize variables to store total planned and actual rows
total_planned_rows = 0
total_actual_rows = 0

# Prepare CSV file for writing
csv_file_path = 'query_rows_info_WL7.csv'
csv_headers = ['Query Number', 'Operator', 'Planned Rows', 'Actual Rows']

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
            if "rows=" in row[0]:
                # Extract the operator name
                parts = row[0].split(' (cost=')
                operator = parts[0].strip()

                # Find and extract the planned rows part
                rows_index = row[0].find("rows=") + len("rows=")
                rows_part = row[0][rows_index:].split(" ")[0]
                planned_rows = rows_part.split()[0]

                # Handle cases where actual rows may be strings like '(never executed)'
                actual_rows_index = row[0].find("rows=", rows_index) + len("rows=")
                actual_rows_part = row[0][actual_rows_index:]
                actual_rows = actual_rows_part.split(" ")[0]

                # If actual rows is not a digit, set it to zero
                if not actual_rows.isdigit():
                    actual_rows = 0

                # Convert rows to integer and add to total
                total_planned_rows += int(planned_rows)
                total_actual_rows += int(actual_rows)

                # Print the result with query number and operator
                print(f"{query_number} {operator}: Planned Rows: {planned_rows} Actual Rows: {actual_rows}")

                # Write the result to the CSV file
                writer.writerow([query_number, operator, planned_rows, actual_rows])

# Write total rows to the CSV file
with open(csv_file_path, mode='a', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Total Planned Rows', total_planned_rows])
    writer.writerow(['Total Actual Rows', total_actual_rows])

# Print the total planned and actual rows
print(f"Total Planned Rows: {total_planned_rows}")
print(f"Total Actual Rows: {total_actual_rows}")

# Close the cursor and connection
if cursor:
    cursor.close()
if conn:
    conn.close()

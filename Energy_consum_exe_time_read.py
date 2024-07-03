import psycopg2
import csv
from datetime import datetime
import subprocess
import re
import time


# Function to run powercfg /batteryreport and capture the output file
def run_battery_report(filename):
    subprocess.run(["powercfg", "/batteryreport", f"/output", filename], check=True)

# Function to read queries from an SQL file
def read_queries_from_file(file_path):
    with open(file_path, 'r') as file:
        queries = file.read()

        # Remove comments
        queries = re.sub(r'--.*', '', queries)

        # Split queries based on semicolons
        queries = queries.split(';')
        queries = [query.strip() for query in queries if query.strip()]

        return queries

# Connect to  postgres DB
conn = psycopg2.connect(dbname="postgres", user="postgres", password='*****', port='5432')

# Open a cursor to perform database operations
cur = conn.cursor()

# Read queries from the SQL file
sql_file = 'Workload1.sql'
queries = read_queries_from_file(sql_file)

# Run battery report before starting the workload
start_battery_report = "battery_rep_start_AIndex.html"
run_battery_report(start_battery_report)

# Run queries and log execution times and results
results = []
execution_times = []
total_execution_time = 0
num_queries = len(queries)

for idx, query in enumerate(queries):
    start_time = datetime.now()
    #start_time = time.perf_counter()

    cur.execute(query)
    
    end_time = datetime.now()
    #end_time = time.perf_counter()

    execution_time = (end_time - start_time).total_seconds() #* 1000 #(* 1000) to read in milliseconds
    #execution_time = end_time - start_time

    query_result = cur.fetchall()  # Fetch the results of the query
    results.append((idx + 1, query_result))  # Use query number (index + 1)
    execution_times.append((idx + 1, execution_time))  # Use query number (index + 1)
    total_execution_time += execution_time
    average_execution_time = total_execution_time / num_queries

    # Run battery report at the end of the workload
    if idx == len(queries) - 1:
        end_battery_report = "battery_rep_end_AIndex.html"
        run_battery_report(end_battery_report)                

# Close communication with the database
cur.close()
conn.close()

# Export query results to CSV
with open('query_results_AIndex.csv', 'w', newline='') as results_file:
    csvwriter = csv.writer(results_file)
    csvwriter.writerow(['query_number', 'results'])
    for query_number, query_result in results:
        # Format the query results as a string to write to CSV
        formatted_result = str(query_result)
        csvwriter.writerow([query_number, formatted_result])
        csvwriter.writerow(['\n'])

# Export query execution times to CSV
with open('exe_times_BIndex.csv', 'w', newline='') as times_file:
    csvwriter = csv.writer(times_file)
    csvwriter.writerow(['query_number', 'execution_time'])
    for query_number, execution_time in execution_times:
        csvwriter.writerow([query_number, execution_time])
        csvwriter.writerow(['\n'])
    csvwriter.writerow(['Total Execution Time:', total_execution_time])
    csvwriter.writerow(['Average Execution Time:', average_execution_time])
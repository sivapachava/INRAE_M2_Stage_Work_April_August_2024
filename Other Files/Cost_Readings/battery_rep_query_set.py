import psycopg2
import csv
from datetime import datetime
import subprocess

# Function to run powercfg /batteryreport and capture the output file
def run_battery_report(filename):
    subprocess.run(["powercfg", "/batteryreport", f"/output", filename], check=True)

# Connect to your postgres DB
conn = psycopg2.connect(dbname="postgres", user="postgres", password='manvim', port='5432')

# Open a cursor to perform database operations
cur = conn.cursor()

# List of queries to run
queries = [
"""SELECT data->>'data-temperature' AS TempValue 
FROM connecsens.json_montoldre_row;""",
"""SELECT data->>'data-temperature' AS TempValue 
FROM connecsens.json_montoldre_row WHERE (data->>'data-temperature')::float > 50;""",
"""SELECT f.file_name AS JSONFileName, r.data->>'data-temperature' AS TempValue 
FROM connecsens.json_file f JOIN connecsens.json_montoldre_row r ON f.id = r.file_id WHERE (r.data->>'data-temperature')::float > 50;""",
"""SELECT data->>'data-temperature'AS TempValue, COUNT(*) AS TempCount 
FROM connecsens.json_montoldre_row GROUP BY data->>'data-temperature';""",
"""SELECT data->>'data-temperature'AS TempValue 
FROM connecsens.json_montoldre_row GROUP BY data->>'data-temperature';"""
]

# Run battery report before starting the workload
start_battery_report = "battery_report_start.html"
run_battery_report(start_battery_report)

# Run queries and log execution times
results = []

for idx, query in enumerate(queries):
    start_time = datetime.now()
    #print(f"Start time for query '{query}': {start_time.isoformat()}")
    
    cur.execute(query)
    
    end_time = datetime.now()
    #print(f"End time for query '{query}': {end_time.isoformat()}")
    
    execution_time = (end_time - start_time).total_seconds()
    results.append((query, execution_time))

    # Run battery report at the end of the workload
    if idx == len(queries) - 1:
        end_battery_report = "battery_report_end.html"
        run_battery_report(end_battery_report)

# Close communication with the database
cur.close()
conn.close()

# Export to CSV
with open('query_times_and_battery_reports.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['query', 'execution_time'])
    csvwriter.writerows(results)
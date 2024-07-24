import psycopg2
import csv

# Function to read queries from a .sql file
def read_queries_from_file(file_path):
    with open(file_path, 'r') as file:
        queries = file.read().split(';')
    return [query.strip() for query in queries if query.strip()]

# Connect to  PostgreSQL DB
conn = psycopg2.connect(dbname="postgres", user="postgres", password='*****', port='5432')

# Open a cursor to perform database operations
cur = conn.cursor()

# Specify the path to SQL file
sql_file_path = "Workload1.sql"

# Get queries from the SQL file
queries = read_queries_from_file(sql_file_path)

# Output CSV file
output_file = "all_output.csv"

with open(output_file, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    for query in queries:
        cur.execute(query)
        results = cur.fetchall()
        
        # Write a section header for each query
        csvwriter.writerow([f"Results of query: {query}"])
        
        # Get column names
        column_names = [desc[0] for desc in cur.description]
        # Write column headers
        csvwriter.writerow(column_names)  
        
        # Write the data rows
        csvwriter.writerows(results)
        
        # Add an empty line for separation
        csvwriter.writerow([])

# Close the cursor and connection
cur.close()
conn.close()

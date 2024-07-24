import psycopg2
import csv

# Connect to postgres DB
conn = psycopg2.connect(dbname="postgres", user="postgres", password='*****', port='5432')

# Open a cursor to perform database operations
cur = conn.cursor()

# List of queries to run
queries = [
    "SELECT * FROM connecsens.json_montoldre_row LIMIT 5",
    "SELECT COUNT(*) FROM connecsens.json_montoldre_row"
]

# Output CSV file
output_file = "all_output.csv"

with open(output_file, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    
    for query in queries:
        cur.execute(query)
        results = cur.fetchall()
        
        # Write a section header for each query
        csvwriter.writerow([f"Results of query: {query}"])
        
        # Get column names for the first query
        if "LIMIT 5" in query:
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

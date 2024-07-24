import psycopg2
import csv

# Connect to your PostgreSQL DB
conn = psycopg2.connect(dbname="postgres", user="postgres", password='manvim', port='5432')

# Open a cursor to perform database operations
cur = conn.cursor()

# List of queries to run with their corresponding output filenames
queries = [
    ("""SELECT data, file_id FROM connecsens.json_montoldre_row 
        WHERE data ->> 'data-CNSSRFDataTypeName' LIKE 'TempDegC'
        AND CAST(data ->> 'data-node-timestampUTC' AS Timestamp)
            BETWEEN SYMMETRIC '2024-02-10' AND '2024-05-10'
        ORDER BY data ->> 'data-node-timestampUTC' DESC""", "output1.csv"),
    
    ("""SELECT data FROM connecsens.json_montoldre_row
        WHERE CAST(data ->> 'data-node-timestampUTC' AS Timestamp)::date
            BETWEEN SYMMETRIC '2023-05-14' AND '2023-10-02'
        ORDER BY data ->> 'data-node-timestampUTC' DESC""", "output2.csv")
]

for query, filename in queries:
    cur.execute(query)
    results = cur.fetchall()
    
    # Get column names for the query
    column_names = [desc[0] for desc in cur.description]
    
    # Write results to CSV
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Write column names as the header
        csvwriter.writerow(column_names)
        
        # Write the data rows
        csvwriter.writerows(results)

# Close the cursor and connection
cur.close()
conn.close()

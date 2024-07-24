import psycopg2

def read_queries_from_file(file_path):
    with open(file_path, 'r') as file:
        queries = file.read().split(';')
    return [query.strip() for query in queries if query.strip()]

# Connect to postgres DB
conn = psycopg2.connect(dbname = "postgres", user = "postgres", password = '*****', port = '5432' )
#conn = psycopg2.connect(host= ‘localhost’, dbname = ‘postgres’, user = ‘postgres’, password = ‘’, port = 5432)

# Open a cursor to perform database operations
cur = conn.cursor()

# Specify the path to SQL file
sql_file_path = "Workload1.sql"

# Get queries from the SQL file
queries = read_queries_from_file(sql_file_path)

for query in queries:
    cur.execute(query)
    results = cur.fetchall()
    for row in results:
        print(row)
# Close the cursor and connection
cur.close()
conn.close()

#for query in queries:
    #cur.execute(query)
    #result = cur.fetchone()
    #print(result)

# Commit the transaction (if any changes were made)
#conn.commit()


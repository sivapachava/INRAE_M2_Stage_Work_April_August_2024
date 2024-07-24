import psycopg2

def get_frequent_predicates(conn):
    #query (the text of the SQL query) and calls (the number of times the query was executed)
    #Filters the results to include only queries that start with the keyword 'SELECT' and that have been executed more than 10 times (calls)
    query = """
    SELECT query, calls 
    FROM pg_stat_statements
    WHERE query LIKE  'SELECT%' AND calls > 5
    ORDER BY calls DESC
    LIMIT 5;
    """

    with conn.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall()
    return results

conn = psycopg2.connect(dbname="postgres", user="postgres", password='manvim', port='5432')
frequent_queries = get_frequent_predicates(conn)
print(frequent_queries)
conn.close()
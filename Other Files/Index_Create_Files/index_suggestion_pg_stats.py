import psycopg2
import re

def get_frequent_predicates(conn):
    #query (the text of the SQL query) and calls (the number of times the query was executed)
    #Filters the results to include only queries that start with the keyword 'SELECT' and that have been executed more than 10 times (calls)
    query = """
    SELECT query, calls 
    FROM pg_stat_statements
    WHERE query LIKE 'SELECT%' AND calls > 2
    ORDER BY calls DESC
    LIMIT 10;
    """

    with conn.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall()
    return results

conn = psycopg2.connect(dbname="postgres", user="postgres", password='manvim', port='5432')
frequent_queries = get_frequent_predicates(conn)
#print(frequent_queries)
conn.close()



def suggest_partial_indexes(queries):
    predicates = []
    for query, _ in queries:
        # Extract WHERE clause using regex
        where_clause = re.search(r'WHERE\s+(.*?)(GROUP BY|ORDER BY|LIMIT|$)', query, re.IGNORECASE)
        if where_clause:
            predicates.append(where_clause.group(1))
    return predicates

partial_index_suggestions = suggest_partial_indexes(frequent_queries)
print(partial_index_suggestions)

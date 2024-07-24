import psycopg2
import time

def create_index(conn, index_name, table, column, predicate=None):
    with conn.cursor() as cur:
        if predicate:
            create_index_query = f"CREATE INDEX {index_name} ON {table} ({column}) WHERE {predicate}"
        else:
            create_index_query = f"CREATE INDEX {index_name} ON {table} ({column})"
        
        start_time = time.time()
        cur.execute(create_index_query)
        conn.commit()
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"Index {index_name} created in {duration:.2f} seconds.")

# Connect to your database
conn = psycopg2.connect(dbname="postgres", user="postgres", password='******', port='5432')

# Create the index and measure the time
create_index(conn, "test_idx_on_montoldre", "connecsens.json_montoldre_row", "(data ->> 'data-node-timestampUTC')")

conn.close()
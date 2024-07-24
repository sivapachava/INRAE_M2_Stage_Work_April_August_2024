import psycopg2

def explain_analyze_query(conn, query):
    with conn.cursor() as cur:
        cur.execute(f"EXPLAIN ANALYZE {query}")
        plan = cur.fetchall()
    return plan

def extract_times(plan):
    initial_times = []
    final_times = []
    for line in plan:
        if 'actual time=' in line[0]:
            # Extracting actual time from the query plan
            time_part = line[0].split('actual time=')[1]
            times = time_part.split('..')
            initial_time = float(times[0].split(' ')[0])
            final_time = float(times[1].split(' ')[0])
            initial_times.append(initial_time)
            final_times.append(final_time)
    return initial_times, final_times

def measure_query_performance(conn, queries):
    performance = {}
    for i, query in enumerate(queries):
        plan = explain_analyze_query(conn, query)
        initial_times, final_times = extract_times(plan)
        performance[f"Q{i+1}"] = {
            "Initial Times": initial_times,
            "Final Times": final_times
        }
    return performance

conn = psycopg2.connect(dbname="postgres", user="postgres", password='manvim', port='5432')

queries = [
    "SELECT DISTINCT data ->> 'data-CNSSRFDataTypeName' FROM connecsens.json_montoldre_row;"
]

performance = measure_query_performance(conn, queries)
for query, times in performance.items():
    initial_times = times["Initial Times"]
    final_times = times["Final Times"]
    for i in range(len(initial_times)):
        print(f"{query} actual time Initial {i+1}: {initial_times[i]}")
        print(f"{query} actual time Final {i+1}: {final_times[i]}")

conn.close()

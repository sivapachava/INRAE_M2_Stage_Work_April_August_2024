import psycopg2
from datetime import datetime
import subprocess

def run_battery_report(filename):
    subprocess.run(["powercfg", "/batteryreport", "/output", filename], check=True)

# Establishing the connection
conn = psycopg2.connect(dbname="postgres", user="postgres", password='*****', port='5432')

def create_index(conn, index_name, table, column, predicate=None):
    start_time = datetime.now()
    start_battery_report = "battery_report_start.html"
    run_battery_report(start_battery_report)
    
    with conn.cursor() as cur:
        if predicate:
            create_index_query = f"CREATE INDEX {index_name} ON {table} USING btree (({column}::text)) WHERE {predicate}"
        else:
            create_index_query = f"CREATE INDEX {index_name} ON {table} USING btree (({column}::text))"
        cur.execute(create_index_query)
        conn.commit()
    
    end_time = datetime.now()
    
    end_battery_report = "battery_report_end.html"
    run_battery_report(end_battery_report)

    time_taken = end_time - start_time
    print(f"Index {index_name} created on {table} in {time_taken}. Start battery report: {start_battery_report}, End battery report: {end_battery_report}")

# Example: Creating partial indexes
create_index(conn, "index_data_type_name", "connecsens.json_montoldre_row", "data ->> 'data-CNSSRFDataTypeName'")
import psycopg2

conn = psycopg2.connect(dbname="cebanewdata", user="postgres", password='manvim', port='5432')


def create_index(conn, index_name, table, column, predicate=None):
    with conn.cursor() as cur:
        if predicate:
            #create_index_query = f"CREATE INDEX {index_name} ON {table} USING btree ((({column})::float)) WHERE {predicate}"
            #create_index_query = f"CREATE INDEX {index_name} ON {table} USING btree (({column}::text)) WHERE {predicate}"
            create_index_query = f"""CREATE INDEX {index_name} ON {table} USING btree (({column})) WHERE {predicate}"""
        else:
            #create_index_query = f"CREATE INDEX {index_name} ON {table} USING btree ((({column})::float))"
            #create_index_query = f"CREATE INDEX {index_name} ON {table} USING btree (({column}::text))"
            create_index_query = f"""CREATE INDEX {index_name} ON {table} USING btree (({column}))"""
        cur.execute(create_index_query)
        conn.commit()

# Example: Creating partial indexes
#create_index(conn, "index_data_temp_value", "connecsens.json_montoldre_row", "data ->> 'data-temperature'")
#create_index(conn, "index_data_CNSSRFName", "connecsens.json_montoldre_row", "data ->> 'data-CNSSRFDataTypeName'")
#create_index(conn, "index_data_TimeStampUTC", "connecsens.json_montoldre_row", "data ->> 'data-node-timestampUTC'")
create_index(conn, "index_data_servertimestamp", "connecsens.json_montoldre_row", "data ->> 'servertimestampUTC'")
create_index(conn, "index_data_nodevoltage", "connecsens.json_montoldre_row", "data ->> 'data-node-batteryVoltage'")

conn.close()

#CREATE INDEX index_data_CNRSSName ON connecsens.json_montoldre_row USING btree ((data ->> 'data-CNSSRFDataTypeName'));
#CREATE INDEX index_data_temperature_value ON connecsens.json_montoldre_row USING btree ((data ->> 'data-node-timestampUTC'));
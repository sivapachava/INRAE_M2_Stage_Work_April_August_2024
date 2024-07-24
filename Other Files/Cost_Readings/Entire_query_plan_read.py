import psycopg2

queries = [
    "SELECT data ->> 'data-CNSSRFDataTypeName' FROM connecsens.json_montoldre_row WHERE data ->> 'data-node-timestampUTC' > '2024-02-01';",
    "SELECT data ->> 'data-node-timestampUTC' FROM connecsens.json_montoldre_row WHERE data ->> 'data-CNSSRFDataTypeName' = 'TempDegC';",
    """SELECT
TO_DATE(TO_CHAR(CAST(data ->> 'servertimestampUTC' AS Timestamp) :: DATE, 
	' yyyyMMdd') ,'yyyyMMdd') AS dateServer,
data ->> 'applicationName' AS AppName,
COUNT(DISTINCT data ->> 'devEUI') AS NbDevEUI
FROM connecsens.json_montoldre_row
GROUP BY dateServer, AppName ORDER BY dateServer""",

"""SELECT data ->> 'devEUI' AS DevEUI,
COUNT(data ->> 'devEUI') AS NbTrames
FROM connecsens.json_montoldre_row
WHERE CAST(data ->> 'servertimestampUTC' AS Timestamp) 
	NOT BETWEEN '2019-12-20' AND '2020-01-10'
GROUP BY DevEUI ORDER BY DevEUI"""
]


    # Connect to PostgreSQL
conn = psycopg2.connect(dbname="postgres", user="postgres", password='*****', port='5432')
cursor = conn.cursor()


    # Loop through each query
for query in queries:
        # Execute EXPLAIN ANALYZE for the query
        cursor.execute("EXPLAIN ANALYZE " + query)

        # Fetch and print the execution plan
        rows = cursor.fetchall()
        
        for row in rows:
            print(row[0])

    # Close the cursor and connection
if cursor:
        cursor.close()
if conn:
        conn.close()

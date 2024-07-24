import re

queries = [
"""SELECT data ->> 'data-CNSSRFDataTypeName' AS DataTypeName,
	COUNT(*) AS DataTypeNameCount
	FROM connecsens.json_montoldre_row 	
	WHERE data ->> 'data-CNSSRFDataTypeName' like '%%'
	GROUP BY data ->> 'data-CNSSRFDataTypeName'
	ORDER BY DataTypeNameCount ASC;""",

    """SELECT data ->> 'devEUI' AS devEUI,
COUNT(data ->> 'devEUI') AS nbLignes
FROM connecsens.json_montoldre_row, connecsens.json_file
WHERE json_file.file_name like 'data20240407.json'
AND json_montoldre_row.file_id = json_file.id
GROUP BY devEUI ORDER BY nbLignes""",

"""SELECT DISTINCT data ->> 'applicationName' AS NOM,
COUNT(DISTINCT data ->> 'devEUI') AS DEVEUI
FROM connecsens.json_montoldre_row
ORDER BY NOM""",

"""SELECT data ->> 'applicationName' AS AppName,
COUNT(DISTINCT data ->> 'devEUI') AS NbDevEUI
FROM connecsens.json_montoldre_row
WHERE CAST( data ->> 'servertimestampUTC' AS Timestamp) 
	BETWEEN '2019-01-01' AND '2020-01-20'
GROUP BY AppName""",

"""SELECT data ->> 'devEUI' AS devEUI,
CAST (data ->> 'servertimestampUTC' AS date) AS dateServer,
COUNT(data ->> 'devEUI') AS NbTrames
FROM connecsens.json_montoldre_row
GROUP BY dateServer, devEUI ORDER BY dateServer""",

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
GROUP BY DevEUI ORDER BY DevEUI""",

"""SELECT DISTINCT data->>'data-CNSSRFDataTypeId'
FROM connecsens.json_montoldre_row;""",

"""SELECT SUM((data->>'data-temperature')::float)
FROM connecsens.json_montoldre_row;""",

"""SELECT AVG((data->>'data-illuminance')::float)
FROM connecsens.json_montoldre_row;""",

"""SELECT MAX((data->>'data-node-batteryVoltage')::float)
FROM connecsens.json_montoldre_row;""",

"""SELECT MIN((data->>'data-depth1-soilWaterTension')::float)
FROM connecsens.json_montoldre_row;""",

"""SELECT data->>'data-node-geoPos-latitude', data->>'data-node-geoPos-longitude'
FROM connecsens.json_montoldre_row
WHERE (data->>'data-node-geoPos-latitude')::float > 45.0
AND (data->>'data-node-geoPos-longitude')::float < 7.5;"""
]

for query in queries:
    col_match = re.findall(r'SELECT\s+(?:DISTINCT\s+)?(?:\s*(\w+)\s*|\(?(.*?)\)?)\s+(?:AS\s+\w+\s+)?FROM', query, re.IGNORECASE | re.DOTALL)
    table_match = re.findall(r'FROM\s+([\w\.\s,]+)', query, re.IGNORECASE)
    join_match = re.findall(r'JOIN\s+([\w\.\s,]+)\s+ON\s+(.*?)(?:\s+WHERE|\s+GROUP BY|\s+ORDER BY|\s+LIMIT|$)', query, re.IGNORECASE | re.DOTALL)
    where_match = re.findall(r'WHERE\s+(.*?)(GROUP BY|ORDER BY|LIMIT|$)', query, re.IGNORECASE | re.DOTALL)
    field_match = re.findall(r"data\s*->>\s*'([^']+)'", query, re.IGNORECASE)

    col_names = []
    table_names = []
    field_names = []

    if col_match:
        for col_tuple in col_match:
            col = col_tuple[0] if col_tuple[0] else col_tuple[1]
            if 'SUM(' not in col and 'AVG(' not in col and 'MAX(' not in col and 'MIN(' not in col:
                if 'data ->>' not in col and 'data->>' not in col:
                    col_names.append(col.strip())

    if table_match:
        raw_tables = re.split(r',\s*', table_match[0].replace('\n', ' ').strip())
        for table in raw_tables:
            table = re.split(r'\s+(WHERE|GROUP BY|ORDER BY|LIMIT|JOIN)\b', table)[0].strip()
            table_names.append(table)

    if join_match:
        for join in join_match:
            table_names.append(join[0].strip())
            on_clause = join[1]
            on_cols = re.findall(r'\b(\w+\.\w+)\b', on_clause)
            col_names.extend(on_cols)

    if where_match:
        where_cols = re.split(r'\s+AND\s+', where_match[0][0].replace('\n', ' ').strip())
        for col in where_cols:
            match = re.search(r'\b(\w+\.\w+)\b', col)
            if match:
                col_names.append(match.group(1))
                equals_match = re.findall(r'(\w+\.\w+)\s*=\s*(\w+\.\w+)', col)
                for eq_match in equals_match:
                    col_names.extend(eq_match)

    if field_match:
        field_names = field_match

    # Remove duplicates from col_names
    col_names = list(set(col_names))

    print(f"Columns: {col_names}")
    print(f"Tables: {table_names}")
    print(f"Fields: {field_names}")
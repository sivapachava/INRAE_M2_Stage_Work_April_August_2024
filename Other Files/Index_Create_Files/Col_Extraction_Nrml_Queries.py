import re

queries = [
"""SELECT data ->> 'devEUI' AS devEUI,
COUNT(data ->> 'devEUI') AS nbLignes
FROM connecsens.json_montoldre_row, connecsens.json_file
WHERE json_file.file_name like 'data20240407.json'
GROUP BY devEUI ORDER BY nbLignes""",

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
GROUP BY DevEUI ORDER BY DevEUI"""
]


for query in queries:
    col_match = re.findall(r'SELECT\s+(.*?)\s+FROM', query, re.IGNORECASE | re.DOTALL)
    table_match = re.findall(r'FROM\s+([\w\.\s,]+)', query, re.IGNORECASE)
    where_match = re.findall(r'WHERE\s+(.*?)(GROUP BY|ORDER BY|LIMIT|$)', query, re.IGNORECASE | re.DOTALL)
    field_match = re.findall(r"data\s*->>\s*'([^']+)'", query, re.IGNORECASE)

    col_names = []
    table_names = []
    field_names = []

    if col_match:
        raw_cols = re.split(r',\s*', col_match[0].replace('\n', ' ').strip())

        for col in raw_cols:
            if 'data ->>' not in col and 'yyyyMMdd' not in col:
                col_names.append(col.strip())

    if where_match:
        where_cols = re.split(r'\s+AND\s+', where_match[0][0].replace('\n', ' ').strip())
        for col in where_cols:
            # Match columns in the form of `table.column`
            match = re.search(r'\b(\w+\.\w+)\b', col)
            if match:
                col_names.append(match.group(1))
            # Also match columns in the form of `table.column = table.column`
            equals_match = re.findall(r'(\w+\.\w+)\s*=\s*(\w+\.\w+)', col)
            for eq_match in equals_match:
                col_names.extend(eq_match)

    if table_match:
        raw_tables = re.split(r',\s*', table_match[0].replace('\n', ' ').strip())
        for table in raw_tables:
            # Remove any trailing content that starts with WHERE, GROUP BY, ORDER BY, or LIMIT
            table = re.split(r'\s+(WHERE|GROUP BY|ORDER BY|LIMIT|JOIN)\b', table)[0].strip()
            table_names.append(table)

    if field_match:
        field_names = field_match

    # Remove duplicates from col_names
    col_names = list(set(col_names))

    print(f"Columns: {col_names}")
    print(f"Tables: {table_names}")
    print(f"Fields: {field_names}")
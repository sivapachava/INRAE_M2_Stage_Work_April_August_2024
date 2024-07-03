-- Query 1: Simple SELECT (Get all 'data-temperature' values from montoldre, Total rows - 2235825)
SELECT data->>'data-temperature' AS TempValue
FROM connecsens.json_montoldre_row;

-- Query 2: Simple SELECT with WHERE clause (Get all 'data-temperature' values from montoldre > 50, Total rows - 229)
SELECT data->>'data-temperature' AS TempValue
FROM connecsens.json_montoldre_row
WHERE (data->>'data-temperature')::float > 50.0;

-- Query 3: SELECT with JOIN (Get all 'data-temperature' values from montoldre > 50 along with file names, Total rows - 229)
SELECT f.file_name AS JSONFileName, 
r.data->>'data-temperature' AS TempValue
FROM connecsens.json_file f
JOIN connecsens.json_montoldre_row r ON f.id = r.file_id
WHERE (r.data->>'data-temperature')::float > 50.0;

-- Query 4: GROUP BY with aggregation (Get all 'data-temperature' values from montoldre with how many times we have same temperature value in montoldre, Total rows - 733)
SELECT data->>'data-temperature' AS TempValue, COUNT(*) AS TempCount
FROM connecsens.json_montoldre_row
GROUP BY data->>'data-temperature';

-- Query 5: SELECT with GROUP BY (Get all 'data-temperature' values from montoldre GROUP BY same temperature value, Total rows - 733)
SELECT data->>'data-temperature'AS TempValue
FROM connecsens.json_montoldre_row
GROUP BY data->>'data-temperature';

-- Query 6: SELECT with GROUP BY with ORDER BY (Get all 'data-temperature' values from montoldre with how many times we have same temperature value in montoldre in ASC order, Total rows - 733)
SELECT data->>'data-temperature'AS TempValue, COUNT(*) AS TempCount
FROM connecsens.json_montoldre_row
GROUP BY data->>'data-temperature'
ORDER BY COUNT(*) ASC;

-- Query 7: SELECT with ORDER BY (Get all 'data-temperature' values from montoldre in ASC order, Total rows - 2235825)
SELECT data->>'data-temperature' AS TempValue
FROM connecsens.json_montoldre_row
ORDER BY (data->>'data-temperature')::float ASC;

-- Query 8: SELECT with multiple WHERE conditions (Get all 'data-temperature' values from montoldre in bewteen 45.0 to 75.0, Total rows - 456)
SELECT data->>'data-temperature' AS TempValue
FROM connecsens.json_montoldre_row
WHERE (data->>'data-temperature')::float > 45.0
AND (data->>'data-temperature')::float < 75.0;

-- Query 9: SELECT with LIKE operator (Get all 'data-temperature' values from montoldre WHERE 'data-CNSSRFDataTypeName' like 'TempDegC', Total rows - 732)
SELECT data->>'data-temperature' AS TempValue
FROM connecsens.json_montoldre_row
WHERE data ->> 'data-CNSSRFDataTypeName' LIKE 'TempDegC' 
GROUP BY data->>'data-temperature';

-- Query 10: SELECT DISTINCT (Get all DISTINCT 'data-temperature' values from montoldre, Total rows - 733)
SELECT DISTINCT data->>'data-temperature' AS TempValue
FROM connecsens.json_montoldre_row;

-- Query 11: SELECT with JOIN and WHERE (Get all json file names for a given application name with 'data-temperature' values, Total rows - 2235825)
SELECT f.file_name AS JsonFileName, 
r.data->>'data-temperature' AS TempValue
FROM connecsens.json_file f
JOIN connecsens.json_montoldre_row r ON f.id = r.file_id
WHERE f.app_name like 'Montoldre';

-- Query 12: SUM aggregation (Get SUM of 'data-temperature' values from montoldre, Total rows - 1)
SELECT SUM((data->>'data-temperature')::float) AS total_temp
FROM connecsens.json_montoldre_row;

-- Query 13: AVG aggregation (Get AVG of 'data-temperature' values from montoldre, Total rows - 1)
SELECT AVG((data->>'data-temperature')::float) AS avg_temp
FROM connecsens.json_montoldre_row;

-- Query 14: MAX aggregation (Get MAX 'data-temperature' value from montoldre, Total rows - 1)
SELECT MAX((data->>'data-temperature')::float) AS min_temp
FROM connecsens.json_montoldre_row;

-- Query 15: MIN aggregation (Get MIN 'data-temperature' value from montoldre, Total rows - 1)
SELECT MIN((data->>'data-temperature')::float) AS max_temp
FROM connecsens.json_montoldre_row;

-- Query 16: SELECT with DATE functions (Get all 'data-temperature' values from montoldre FROM '2024-01-01' data-node time, Total rows - 24935)
SELECT data->>'data-temperature' AS TempValue, COUNT(*) AS TempValueCount,
	data->>'data-node-timestampUTC' AS datetime
FROM connecsens.json_montoldre_row
WHERE data->>'data-node-timestampUTC' >= '2024-01-01T00:00:00Z'
GROUP BY data->>'data-node-timestampUTC', data->>'data-temperature';

-- Query 17: SELECT with NULL condiation (Get sum of rows count in montoldre with 'data-temperature' value is NOT NULL, Total rows - 1, rows count - 398019)
SELECT	COUNT(data ->>'data-temperature') AS TempNumber
	FROM  connecsens.json_montoldre_row
	WHERE data ->>'data-temperature' IS NOT NULL;

-- Query 18: SELECT with NULL condiation (Get sum of rows count in montoldre where 'data-temperature' value is zero, Total rows - 1, rows count - 152) 
SELECT	COUNT(data ->>'data-temperature') AS TempNumberNull
	FROM  connecsens.json_montoldre_row
	WHERE (data ->>'data-temperature')::float = 0.0;

-- Query 19: SELECT other JSON field w.r.to 'data-temperature' (Get all 'data-DataChannel' values from montoldre WHERE 'data-temperature' value is > 50,  Total rows - 229) 
SELECT data ->> 'data-DataChannel'
	FROM connecsens.json_montoldre_row
	WHERE (data->>'data-temperature')::float > 50.0;

-- Query 20: SELECT with multiple JOINS (Get all json file names for a given application name with 'data-temperature' values from application name, Total rows - 500000)
SELECT f.file_name AS JsonFileName, 
	r.data->>'data-temperature' AS TempValue,
	s.data->>'data-temperature' AS FinalTempValue, 
	s.data ->> 'applicationName' AS AppliName
FROM connecsens.json_file f
JOIN connecsens.json_montoldre_row r 
	ON f.id = r.file_id
JOIN connecsens.json_montoldre_row s 
	ON f.app_name = s.data->>'applicationName'
LIMIT 500000;
--Query1 (Get sum of rows count in montoldre with 'data-CNSSRFDataTypeName' value is NULL, Total rows - 1, rows count - 171)
-- Count rows with NULL data-CNSSRFDataTypeName
SELECT COUNT(*) AS DataCountWithNull
	FROM connecsens.json_montoldre_row
WHERE (data ->> 'data-CNSSRFDataTypeName') IS NULL;

--Query2 (Get all 'data-CNSSRFDataTypeName' values from montoldre with how many records it has in montoldre for each 'data-CNSSRFDataTypeName', Total rows - 18)
--Count records for each data-CNSSRFDataTypeName
SELECT data ->> 'data-CNSSRFDataTypeName' AS DataTypeName,
	COUNT(*) AS DataTypeNameCount
	FROM connecsens.json_montoldre_row 	
	WHERE data ->> 'data-CNSSRFDataTypeName' like '%%'
	GROUP BY DataTypeName
	ORDER BY DataTypeNameCount ASC;

--Query3 (Get count of DISTINCT values of 'data-CNSSRFDataTypeName' from montoldre, Total rows - 1, count - 18)
--Count DISTINCT data-CNSSRFDataTypeName values
SELECT COUNT(DISTINCT(data ->> 'data-CNSSRFDataTypeName')) AS CNSSRFDataTypeNames
	FROM connecsens.json_montoldre_row 	
	WHERE data ->> 'data-CNSSRFDataTypeName' like '%%';
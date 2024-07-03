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

--Query4 (Get DISTINCT values of 'data-CNSSRFDataTypeName' along with 'data-CNSSRFDataTypeId' values from montoldre, Total rows - 19)
--Get DISTINCT data-CNSSRFDataTypeId and data-CNSSRFDataTypeName pairs
SELECT DISTINCT (data ->> 'data-CNSSRFDataTypeId') AS DataTypeId,
                (data ->> 'data-CNSSRFDataTypeName') AS DataTypeName
FROM connecsens.json_montoldre_row
ORDER BY DataTypeId ASC;

--Query5 (Get DISTINCT values of 'data-CNSSRFDataTypeName' along with 'applicationID' values from montoldre, Total rows - 34)
--Get DISTINCT data-CNSSRFDataTypeName and applicationID pairs
SELECT DISTINCT (data ->> 'applicationID') AS AppliId,
                (data ->> 'data-CNSSRFDataTypeName') AS DataTypeName
FROM connecsens.json_montoldre_row;

--Query6 (Get all 'data-node-timestampUTC' values from montoldre where 'data-temperature' value is > 50 for 'data-CNSSRFDataTypeName' is 'TempDegC', Total rows - 229) 
--Get data-node-timestampUTC for temperatures > 50 where data-CNSSRFDataTypeName is 'TempDegC'
SELECT data ->> 'data-node-timestampUTC' 
	FROM connecsens.json_montoldre_row 
WHERE data ->> 'data-CNSSRFDataTypeName' like 'TempDegC'
    AND 
        (data ->> 'data-temperature')::float > 50
    ORDER BY data ->> 'data-temperature' ASC;

--Query7 (Get data from montoldre for a particular time interval, Total rows - 17746)
--Get data for 'TempDegC' within a specific time range
SELECT data 
	FROM connecsens.json_montoldre_row 
WHERE data ->> 'data-CNSSRFDataTypeName' like 'TempDegC'
    AND CAST(data ->> 'data-node-timestampUTC' as Timestamp)
        BETWEEN SYMMETRIC '2024-01-01' AND '2024-04-30'
    ORDER BY
        data ->> 'data-node-timestampUTC' desc;

--Query8 (Get count of each 'data-DataChannel' records count from a given application, Total rows - 7)
--Count data-DataChannel records for a given devEUI
SELECT data ->> 'data-DataChannel' AS dataChannel,
COUNT(data ->> 'data-DataChannel') AS dataChannelCount
FROM connecsens.json_montoldre_row
WHERE data ->>'devEUI' like '434e535303e36201'
GROUP BY dataChannel;

--Query9 (Get the number of records by 'devEUI' along with 'servertimestampUTC', Total rows - 4081)
--Count records by devEUI and servertimestampUTC
SELECT data ->> 'devEUI' AS DeviceIdentifier,
CAST (data ->> 'servertimestampUTC' AS date) AS dateServer,
COUNT(data ->> 'devEUI') AS NbTrames
FROM connecsens.json_montoldre_row
GROUP BY dateServer, DeviceIdentifier ORDER BY dateServer;

--Query10 (Get the number of records per day from  '2023-01-01', Total rows - 502)
--Count records per day since '2023-01-01'
SELECT data ->> 'data-node-timestampUTC' AS DataNodeDay,
    COUNT(*) AS RecordsPerDay
FROM connecsens.json_montoldre_row
WHERE data ->> 'data-node-timestampUTC' > '2023-01-01'
GROUP BY data->>'data-node-timestampUTC'
ORDER BY DataNodeDay;


--Query11 (checking how many different ConfigMM3Hash32 values we have for each devEUI along with 'data-CNSSRFDataTypeName' names in each configuration, Total rows - 386)
--Count ConfigMM3Hash32 values for each devEUI with data-CNSSRFDataTypeName
SELECT data ->> 'devEUI' AS DeviceIdentifier,
data ->> 'data-CNSSRFConfigMM3Hash32' AS CNSSRFConfigMM3Hash32,
data ->> 'data-CNSSRFDataTypeName' AS measureName,
MIN(CAST (data ->> 'servertimestampUTC' AS date)) AS FirstApparitionHash,
MAX(CAST (data ->> 'servertimestampUTC' AS date)) AS LastApparitionHash
FROM connecsens.json_montoldre_row
WHERE data ->> 'data-CNSSRFConfigMM3Hash32' != ''
GROUP BY DeviceIdentifier, CNSSRFConfigMM3Hash32, measureName
ORDER BY DeviceIdentifier;

--Query12 (Get count of records in a particular application for a given json file, Total rows - 1, count - 528)
--Count records for a specific JSON file
SELECT COUNT(data)  AS DeviceIdentifier
    FROM connecsens.json_montoldre_row
    JOIN connecsens.json_file ON json_montoldre_row.file_id = json_file.id
    WHERE json_file.file_name = 'data20240407.json';

--Query13 (Get count of records in each json file, Total rows - 1387)
--Count records in each JSON file
SELECT f.file_name AS JsonFileName, r.file_id AS JsonFileNameId, 
	COUNT(r.file_id) AS RecordsInMontoldre
FROM connecsens.json_montoldre_row r
JOIN connecsens.json_file f ON f.id = r.file_id
GROUP BY JsonFileNameId, JsonFileName;

--Query14 (Get all different 'data-CNSSRFDataTypeName' measured names for a particular json file, Total rows - 19)
--Get DISTINCT data-CNSSRFDataTypeName for a specific JSON file
SELECT DISTINCT (data ->> 'data-CNSSRFDataTypeName')  AS DataName
    FROM connecsens.json_montoldre_row r
    JOIN connecsens.json_file ON r.data ->> 'applicationName'= json_file.app_name
    WHERE json_file.file_name = 'data20230407.json';

--Query15 (Get respective values for a particular 'devEUI' to analyze, to how many receivers it send data and to which application, Total rows - 242 )
--Get values for a specific devEUI to analyze receivers and applications
SELECT
data ->> 'applicationName' AS AppliName,
data ->> 'rxInfo-name' AS ReceiverNode,
data ->> 'data-DataChannel' AS DataChannel,
data ->> 'data-CNSSRFDataTypeName' AS DataType
FROM connecsens.json_montoldre_row
WHERE data->>'devEUI' = '434e535303e36217' and data ->> 'data-CNSSRFDataTypeName' != 'config'
GROUP BY DataChannel, ReceiverNode, AppliName, DataType;

--Query16 (Get data for a given application where 'data-CNSSRFDataTypeName' is NULL)
--Get data for applications where data-CNSSRFDataTypeName is NULL
SELECT data 
    FROM connecsens.json_montoldre_row
WHERE data ->> 'data-CNSSRFDataTypeName' IS NULL;

--Query 17 (Get all unique JSON fields in data column)
--Get all unique JSON fields in the data column
SELECT DISTINCT  jsonb_object_keys(data) 
FROM connecsens.json_montoldre_row;

--Query 18 (Get total count of records which have DataTypeName Temperature)
--Count records with data-CNSSRFDataTypeName as 'Temperature'
SELECT data ->> 'data-CNSSRFDataTypeName' AS DatatypeName,
    COUNT(data ->> 'data-CNSSRFDataTypeName') AS numberAppmication
FROM connecsens.json_montoldre_row 
WHERE data ->> 'data-CNSSRFDataTypeName' LIKE '%TempDegC%'
AND CAST(data ->> 'data-node-timestampUTC' AS Timestamp) 
    BETWEEN '2020-01-01' AND '2024-05-15'
GROUP BY data ->> 'data-CNSSRFDataTypeName';

--Query 19 (Get all unique temperature values in every file with the file name they appear in and the applicationName)
--Get unique temperature values with file names and application names
SELECT DISTINCT CAST(data ->> 'data-temperature' AS float) AS ValTemp,
file_name, app_name
FROM connecsens.json_file, connecsens.json_montoldre_row 
WHERE json_file.id = json_montoldre_row.file_id
AND data ->> 'data-CNSSRFDataTypeName' LIKE '%TempDegC%';

--Query 20 (select first and last day at node, receiver and server in data)
--Select first and last dates at node, receiver, and server
SELECT 
MIN(CAST(data ->> 'data-node-timestampUTC' AS Date)) AS dataNode_Date_Min,
MAX(CAST(data ->> 'data-node-timestampUTC' AS Date)) AS dataNode_Date_Max,
MIN(CAST(data ->> 'rxInfo-time' AS Date)) AS rxtime_Date_Min,
MAX(CAST(data ->> 'rxInfo-time' AS Date)) AS rxtime_Date_Max,
MIN(CAST(data ->> 'servertimestampUTC' AS Date)) AS servertime_Date_Min,
MAX(CAST(data ->> 'servertimestampUTC' AS Date)) AS servertime_Date_Max
FROM connecsens.json_montoldre_row;
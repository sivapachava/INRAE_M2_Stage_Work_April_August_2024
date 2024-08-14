-- Query 1 (576 rows - 120 rows)
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-node-batteryVoltage}', '"985.1433"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-11-27T00:08:41.067586' AND '2019-11-27T04:02:46.924740';

-- Query 2 (576 rows - 120 rows)
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-node-batteryVoltage}', '"6536.2175"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-11-29T00:11:15.073677' AND '2019-11-29T04:01:04.895526';

-- Query 3 (576 rows - 120 rows)
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-node-batteryVoltage}', '"7224.3282"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-12-01T00:02:37.011408' AND '2019-12-01T03:59:49.982800';

-- Query 4 (576 rows)
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-node-batteryVoltage}', '"85321.498963"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-12-03T00:10:28.137551' AND '2019-12-03T04:08:53.970996';

-- Query 5 (576 rows)
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-node-batteryVoltage}', '"73452.58785"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-12-05T00:07:24.173771' AND '2019-12-05T04:00:43.162133';
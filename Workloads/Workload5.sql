-- Query 1
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-node-batteryVoltage}', '"3.07"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2020-12-20' AND '2020-12-21';

-- Query 2
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-node-batteryVoltage}', '"3.0"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-11-07' AND '2019-11-08';

-- Query 3
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-temperature}', '"25"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-11-09' AND '2019-11-10';

-- Query 4
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-soilVolumetricWaterContent}', '"3.25"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-11-11' AND '2019-11-12';

-- Query 5
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-depth1-soilWaterTension}', '"355"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-12-09' AND '2019-12-10';

-- Query 6
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-resetSource-name}', '"cebaplatform"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2020-09-13' AND '2020-09-14';

-- Query 7
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-relativeDielectricPermittivity}', '"3.0"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-12-11' AND '2019-12-12';

-- Query 8
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-rainAmount-time}', '"550"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-11-15' AND '2019-11-16';

-- Query 9
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-illuminance}', '"2"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2020-02-23' AND '2020-02-24';

-- Query 10
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-depth}', '"12"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-11-19' AND '2019-11-20';

-- Query 11
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-configValue}', '"700"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-11-21' AND '2019-11-22';

-- Query 12
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-battery-voltage}', '"2.50"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-11-23' AND '2019-11-24';

-- Query 13
UPDATE connecsens.json_montoldre_row
SET data = jsonb_set(data, '{data-airHumidity}', '"40.5"')
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp)
    BETWEEN SYMMETRIC '2020-02-17' AND '2020-02-18';

-- Query 14
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-node-batteryVoltage}', '"3.01"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-11-25' AND '2019-11-26';

-- Query 15
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-node-batteryVoltage}', '"3.02"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-11-27' AND '2019-11-28';

-- Query 16
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-node-batteryVoltage}', '"3.03"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-11-29' AND '2019-11-30';

-- Query 17
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-node-batteryVoltage}', '"3.04"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-12-01' AND '2019-12-02';

-- Query 18
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-node-batteryVoltage}', '"3.05"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-12-03' AND '2019-12-04';

-- Query 19
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-node-batteryVoltage}', '"3.06"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-12-05' AND '2019-12-06';

-- Query 20
UPDATE connecsens.json_montoldre_row 
SET data = jsonb_set(data, '{data-node-batteryVoltage}', '"3.07"') 
WHERE CAST(data ->> 'servertimestampUTC' AS timestamp) 
    BETWEEN SYMMETRIC '2019-12-07' AND '2019-12-08';
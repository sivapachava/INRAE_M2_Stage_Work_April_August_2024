-- Query 1:
SELECT data FROM connecsens.json_montoldre_row
    WHERE data ->> 'data-CNSSRFDataTypeName' like '%TimestampUTC%'
    AND CAST(data ->> 'servertimestampUTC' as Timestamp)
        BETWEEN SYMMETRIC '2019-01-01' AND '2024-05-10';

-- Query 2:
SELECT data FROM connecsens.json_montoldre_row 
    WHERE data ->> 'data-CNSSRFDataTypeName' like '%SoilMoistureCbDegCHz%'
    AND CAST(data ->> 'servertimestampUTC' as Timestamp)
        BETWEEN SYMMETRIC '2019-01-01' AND '2024-05-10';

-- Query 3:
SELECT data FROM connecsens.json_montoldre_row 
    WHERE data ->> 'data-CNSSRFDataTypeName' like '%Config%'
    AND CAST(data ->> 'servertimestampUTC' as Timestamp)
        BETWEEN SYMMETRIC '2019-01-01' AND '2024-05-10';

-- Query 4:
SELECT data FROM connecsens.json_montoldre_row 
    WHERE data ->> 'data-CNSSRFDataTypeName' like '%GeographicalPosition2D%'
    AND CAST(data ->> 'servertimestampUTC' as Timestamp)
        BETWEEN SYMMETRIC '2019-01-01' AND '2024-05-10'
    ORDER BY (data ->> 'servertimestampUTC')::timestamp DESC;

-- Query 5:
SELECT data FROM connecsens.json_montoldre_row 
    WHERE data ->> 'data-CNSSRFDataTypeName' like '%RainAmountMM%'
    AND CAST(data ->> 'servertimestampUTC' as Timestamp)
        BETWEEN SYMMETRIC '2019-01-01' AND '2024-05-10'
    ORDER BY (data ->> 'servertimestampUTC')::timestamp DESC;

-- Query 6:
SELECT data FROM connecsens.json_montoldre_row 
    WHERE data ->> 'data-CNSSRFDataTypeName' like '%AppSoftwareVersionMMPHash32%'
    AND CAST(data ->> 'servertimestampUTC' as Timestamp)
        BETWEEN SYMMETRIC '2019-01-01' AND '2024-05-10';

-- Query 7:
SELECT data FROM connecsens.json_montoldre_row 
    WHERE data ->> 'data-CNSSRFDataTypeName' like '%IlluminanceLux%'
    AND CAST(data ->> 'servertimestampUTC' as Timestamp)
        BETWEEN SYMMETRIC '2019-01-01' AND '2024-05-10';

-- Query 8:
SELECT data FROM connecsens.json_montoldre_row 
    WHERE data ->> 'data-CNSSRFDataTypeName' like '%TruebnerSMT100Raw%'
    AND CAST(data ->> 'servertimestampUTC' as Timestamp)
        BETWEEN SYMMETRIC '2019-01-01' AND '2024-05-10';

-- Query 9:
SELECT data FROM connecsens.json_montoldre_row 
    WHERE data ->> 'data-CNSSRFDataTypeName' like '%RelativeDielectricPermittivity%'
    AND CAST(data ->> 'servertimestampUTC' as Timestamp)
        BETWEEN SYMMETRIC '2019-01-01' AND '2024-05-10';

-- Query 10:
SELECT data FROM connecsens.json_montoldre_row 
    WHERE data ->> 'data-CNSSRFDataTypeName' IS NULL
    AND CAST(data ->> 'servertimestampUTC' as Timestamp)
        BETWEEN SYMMETRIC '2019-01-01' AND '2024-05-10';

-- Query 11:
SELECT data FROM connecsens.json_montoldre_row 
    WHERE data ->> 'data-CNSSRFDataTypeName' like '%SoilVolumetricWaterContentPercent%' 
    AND CAST(data ->> 'servertimestampUTC' as Timestamp) > '2019-01-01';

-- Query 12:
SELECT DISTINCT(data ->> 'data-temperature')
    FROM connecsens.json_montoldre_row 
    WHERE data ->> 'data-CNSSRFDataTypeName' like '%Temp%' 
    AND CAST(data ->> 'servertimestampUTC' as Timestamp) > '2019-01-01';

-- Query 13:
SELECT DISTINCT(data ->> 'data-temperature')
    FROM connecsens.json_montoldre_row 
    WHERE data ->> 'data-CNSSRFDataTypeName' like '%Temp%' 
    AND CAST(data ->> 'servertimestampUTC' as Timestamp) > '2019-01-01';

-- Query 14:
SELECT DISTINCT(data ->> 'data-illuminance')
    FROM connecsens.json_montoldre_row 
    WHERE data ->> 'data-CNSSRFDataTypeName' like '%IlluminanceLux%' 
    AND CAST(data ->> 'servertimestampUTC' as Timestamp) > '2019-01-01';

-- Query 15:
SELECT data ->> 'applicationName' AS AppName,
    COUNT(DISTINCT data ->> 'devEUI') AS NbDevEUI
    FROM connecsens.json_montoldre_row
    WHERE   CAST(data ->> 'servertimestampUTC' as Timestamp)
        BETWEEN SYMMETRIC '2019-01-01' AND '2024-05-10'
    GROUP BY AppName;

-- Query 16:
SELECT data FROM connecsens.json_montoldre_row
    WHERE  CAST(data ->> 'servertimestampUTC' as Timestamp)
        BETWEEN SYMMETRIC '2019-01-01' AND '2024-05-10';

-- Query 17:
SELECT data ->> 'rxInfo-time', 
    data ->> 'data-node-timestampUTC',
    data ->> 'servertimestampUTC' 
    FROM connecsens.json_montoldre_row
    WHERE  CAST(data ->> 'servertimestampUTC' as Timestamp)
        BETWEEN SYMMETRIC '2019-01-01' AND '2024-05-10';
CREATE OR REPLACE FUNCTION estimate_jsonb_field_cardinality(
    schema_name TEXT,
    table_name TEXT,
    jsonb_column TEXT,
    fields TEXT[]
)
RETURNS TABLE(field_name TEXT, estimated_cardinality BIGINT) AS $$
DECLARE
    field TEXT;
    query TEXT;
BEGIN
    FOREACH field IN ARRAY fields
    LOOP
        query := format(
            -- Construct the query for each field to get the estimated cardinality
            'SELECT %L AS field_name, COUNT(DISTINCT %s->>%L) AS estimated_cardinality FROM %I.%I',
            field, jsonb_column, field, schema_name, table_name
        );

        RETURN QUERY EXECUTE query;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


-- Query to get cardinality of any particular field in JSON file
SELECT * FROM estimate_jsonb_field_cardinality(
  'connecsens', 'json_montoldre_row', 'data', 
    ARRAY['devEUI', 'fPort', 'fCnt',......]);

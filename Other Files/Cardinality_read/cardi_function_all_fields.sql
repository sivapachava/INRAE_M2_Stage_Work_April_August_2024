CREATE OR REPLACE FUNCTION estimate_jsonb_field_cardinality(
    schema_name TEXT,
    table_name TEXT,
    jsonb_column TEXT
)
RETURNS TABLE(field_name TEXT, estimated_cardinality BIGINT) AS $$
DECLARE
    field TEXT;
    query TEXT;
BEGIN
    -- Get the list of distinct keys from the JSONB column
    query := format(
        'SELECT DISTINCT jsonb_object_keys(%I) FROM %I.%I',
        jsonb_column, schema_name, table_name
    );

    -- Execute the query to get the list of fields dynamically
    FOR field IN EXECUTE query LOOP
        -- Construct the query for each field to get the estimated cardinality
        query := format(
            'SELECT %L AS field_name, COUNT(DISTINCT %s->>%L) AS estimated_cardinality FROM %I.%I',
            field, jsonb_column, field, schema_name, table_name
        );

        -- Execute and return the query results
        RETURN QUERY EXECUTE query;
    END LOOP;
END;
$$ LANGUAGE plpgsql;


-- query to run to get result
SELECT * FROM estimate_jsonb_field_cardinality(
  'connecsens', 'json_montoldre_row', 'data');
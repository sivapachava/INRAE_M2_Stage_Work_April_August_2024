import re
from itertools import combinations
import csv

class WorkloadAnalyzer:
    def __init__(self, queries):
        self.queries = queries
        self.columns = []

    def extract_columns(self):
        for query in self.queries:

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
                    table = re.split(r'\s+(WHERE|GROUP BY|ORDER BY|LIMIT)\b', table)[0].strip()
                    table_names.append(table)

            if field_match:
                field_names = field_match

            # Remove duplicates from col_names
            col_names = list(set(col_names))

            for col in col_names:
                    self.columns.append((col))
            for field in field_names:
                    self.columns.append((f"data ->> '{field}'"))

        #print(self.columns)
        return self.columns
    
class FrequencyCalculator:
    def __init__(self, columns):
        self.columns = columns

    def calculate_frequency(self):
        frequency_dict = {}
        for col in self.columns:
            # Create a unique key for each column with the table name
            column_key = (col)
            if column_key not in frequency_dict:
                frequency_dict[column_key] = 1
            else:
                frequency_dict[column_key] += 1
        #print(frequency_dict)        
        return frequency_dict
    
class CandidateIndexSelector:
    def __init__(self, frequencies):
        self.frequencies = frequencies

    def select_candidate_indices(self):
        candidate_indices = []

        for column, frequency in self.frequencies.items():
            # Select columns that repeat more than twice
            if frequency >= 7 and '*' not in column and 'COUNT(*)' not in column:  
                candidate_indices.append((column, frequency))

        #print(f"candidate_indices:{candidate_indices}")
        return candidate_indices
    
class CardinalityChecker:
    def __init__(self, cardinality_csv_path):
        self.cardinality = self._parse_cardinality_csv(cardinality_csv_path)
    
    def _parse_cardinality_csv(self, cardinality_csv_path):
        cardinality = {}
        with open(cardinality_csv_path, newline='', encoding='utf-8') as csvfile: #encoding='utf-8-sig') 
            reader = csv.DictReader(csvfile, delimiter=';')

            for row in reader:
                column_name = row.get('column') or row.get('\ufeffcolumn')
                cardinality_value = row.get('cardinality')

                if column_name and cardinality_value:
                    cardinality[column_name] = int(cardinality_value)
                else:
                    print("Invalid row in CSV:", row)

        #print(cardinality)            
        return cardinality

    def check_cardinality(self, candidate_indices):
        CardCount = []

        for column, frequency in candidate_indices:
            column_name = column.split(' ->> ')[-1].strip("'")
            cardinality_value = self.cardinality.get(column_name, None)

            if cardinality_value is not None:
                CardCount.append((column, frequency, cardinality_value))
            else:
                CardCount.append((column, frequency, 'Cardinality not found'))

        #print(CardCount)        
        return CardCount
    
class ProcessIndexSelector:
    def __init__(self, counts):
        self.counts = counts

    def select_process_indices(self):
        process_indices = []
        for column, frequency, count in self.counts:
            if count >= 5:  # Select columns that repeat more than twice
                process_indices.append((column, frequency, count))

        #print(process_indices)
        return process_indices
    
class IndexConfigurationSelector:
    def __init__(self, process_indices):
        self.process_indices = process_indices

    def get_index_configurations(self):
        # Generate all possible index configurations
        all_configurations = []

        for r in range(1, 4):
            all_configurations.extend(combinations(self.process_indices, r))

        #print(all_configurations)
        return all_configurations
    
def main(queries, cardinality_csv_path):
    analyzer = WorkloadAnalyzer(queries)
    columns = analyzer.extract_columns()

    frequency_calculator = FrequencyCalculator(columns)
    frequencies = frequency_calculator.calculate_frequency()

    candidate_index_selector = CandidateIndexSelector(frequencies)
    candidate_indices = candidate_index_selector.select_candidate_indices()

    checker = CardinalityChecker(cardinality_csv_path)
    results = checker.check_cardinality(candidate_indices)

    counter = ProcessIndexSelector(results)
    process_indices = counter.select_process_indices()

    index_configuration_selector = IndexConfigurationSelector(process_indices)
    index_configurations = index_configuration_selector.get_index_configurations()

    # Print configurations
    for config in index_configurations:
        print(config)

# Example usage
if __name__ == "__main__":
    queries = [

"""SELECT
data ->> 'devEUI' AS DevEUI,
data ->> 'data-CNSSRFConfigMM3Hash32' AS Hash,
MIN(CAST (data ->> 'servertimestampUTC' AS date)) AS FirstApparitionHash,
MAX(CAST (data ->> 'servertimestampUTC' AS date)) AS LastApparitionHash
FROM connecsens.json_montoldre_row
WHERE data ->> 'data-CNSSRFConfigMM3Hash32' != ''
GROUP BY DevEUI, Hash
ORDER BY DevEUI""",

"""SELECT data ->> 'data-DataChannel' AS dataChannel,
COUNT(data ->> 'data-DataChannel')
FROM connecsens.json_montoldre_row, connecsens.json_file
WHERE data ->>'devEUI' like '434e535303e36201' 
AND json_file.file_name like 'data20240407.json' 
AND json_montoldre_row.file_id = json_file.id
GROUP BY dataChannel""",

"""SELECT data ->> 'data-DataChannel' AS dataChannel,
COUNT(data ->> 'data-DataChannel')
FROM connecsens.json_montoldre_row
WHERE data ->>'devEUI' like '434e535303e36201'
GROUP BY dataChannel""",

"""SELECT data FROM connecsens.json_montoldre_row
WHERE data ->>'devEUI' like '434e535303e36201'
AND data ->> 'data-DataChannel' like '5'
LIMIT 10""",

"""SELECT DISTINCT data ->> 'data-DataChannel' AS dataChannel
FROM connecsens.json_montoldre_row
WHERE data ->> 'data-DataChannel' != ''""",

"""SELECT CAST (data ->> 'servertimestampUTC' AS date) AS dateServer,
COUNT (DISTINCT data ->> 'devEUI') AS nbDevEUI
FROM connecsens.json_montoldre_row
GROUP BY dateServer ORDER BY dateServer DESC LIMIT  10""",

"""SELECT data ->> 'devEUI' AS DevEUI,
COUNT(data ->> 'devEUI') AS nbLignes
FROM connecsens.json_montoldre_row
GROUP BY DevEUI ORDER BY nbLignes""",

"""SELECT data ->> 'devEUI' AS DevEUI,
COUNT(data ->> 'devEUI') AS nbLignes
FROM connecsens.json_montoldre_row, connecsens.json_file
WHERE json_file.file_name like 'data20240407.json'
GROUP BY DevEUI ORDER BY nbLignes""",

"""SELECT data ->> 'devEUI' AS DevEUI,
COUNT(data ->> 'devEUI') AS nbLignes
FROM connecsens.json_montoldre_row, connecsens.json_file
WHERE json_file.file_name like 'data20240407.json'
AND json_montoldre_row.file_id = json_file.id
GROUP BY DevEUI ORDER BY nbLignes""",

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

"""SELECT data ->> 'devEUI' AS DevEUI,
CAST (data ->> 'servertimestampUTC' AS date) AS dateServer,
COUNT(data ->> 'devEUI') AS NbTrames
FROM connecsens.json_montoldre_row
GROUP BY dateServer, DevEUI ORDER BY dateServer""",

"""SELECT
TO_DATE(TO_CHAR(CAST(data ->> 'servertimestampUTC' AS Timestamp) :: DATE, 
'yyyyMMdd') ,'yyyyMMdd') AS dateServer,
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

"""SELECT data ->> 'devEUI' AS DevEUI,
COUNT(data ->> 'devEUI') AS NbTrames
FROM connecsens.json_montoldre_row
WHERE CAST(data ->> 'servertimestampUTC' AS Timestamp) 
BETWEEN '2019-12-20' AND '2020-01-10'
GROUP BY DevEUI ORDER BY DevEUI""",

"""SELECT * FROM connecsens.json_montoldre_row LIMIT 5000""",

"""SELECT COUNT(*) FROM connecsens.json_montoldre_row""",

""" SELECT data  FROM connecsens.json_montoldre_row  WHERE 
data ->> 'devEUI' like '434e535303e36217'""",

"""SELECT  data,file_id FROM connecsens.json_montoldre_row 
WHERE data ->> 'data-CNSSRFDataTypeName' like 'TempDegC'
AND CAST(data ->> 'data-node-timestampUTC' as Timestamp)
BETWEEN SYMMETRIC '2024-02-10' AND '2024-05-10'
ORDER BY  data ->> 'data-node-timestampUTC' desc""",

"""SELECT  data,app_name  FROM  connecsens.json_montoldre_row
WHERE CAST(data ->> 'data-node-timestampUTC' as Timestamp) ::date
BETWEEN SYMMETRIC '2023-05-14' AND '2023-10-02'
ORDER BY  data ->> 'data-node-timestampUTC' desc""",

"""SELECT data FROM connecsens.json_montoldre_row
WHERE data ->> 'applicationID' like  '6'""",

"""SELECT * FROM connecsens.json_montoldre_row
WHERE data ->> 'data-CNSSRFDataTypeId' like  '28'""",

"""(SELECT data FROM connecsens.json_montoldre_row 
WHERE data ->> 'data-CNSSRFDataTypeName' = 'TempDegC'   LIMIT 10)
UNION ALL
(SELECT data FROM connecsens.json_montoldre_row 
WHERE data ->> 'data-CNSSRFDataTypeName' = 'IlluminanceLux'  LIMIT 10)""",

"""SELECT data ->> 'servertimestampUTC' as server_time 
FROM connecsens.json_montoldre_row  LIMIT 3000""",

"""SELECT data ->> 'adr' as statemnt, data ->> 'fCnt' as ccount, 
data ->> 'fPort' as nnumber, data ->> 'txInfodr' as directory 
FROM connecsens.json_montoldre_row LIMIT 10000"""

]
    cardinality_csv_path = "C:/Users/spachava/Downloads/Code_Files/Index_Selection/cardinality_file_f.csv"
    main(queries, cardinality_csv_path)
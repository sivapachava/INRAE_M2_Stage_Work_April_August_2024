import re
from itertools import combinations
import csv

class WorkloadAnalyzer:
    def __init__(self, queries):
        self.queries = queries
        self.columns = []

    def extract_columns(self):
        for query in self.queries:

            col_match = re.findall(r'SELECT\s+(?:DISTINCT\s+)?(?:\s*(\w+)\s*|\(?(.*?)\)?)\s+(?:AS\s+\w+\s+)?FROM', query, re.IGNORECASE | re.DOTALL)
            table_match = re.findall(r'FROM\s+([\w\.\s,]+)', query, re.IGNORECASE)
            join_match = re.findall(r'JOIN\s+([\w\.\s,]+)\s+ON\s+(.*?)(?:\s+WHERE|\s+GROUP BY|\s+ORDER BY|\s+LIMIT|$)', query, re.IGNORECASE | re.DOTALL)
            where_match = re.findall(r'WHERE\s+(.*?)(GROUP BY|ORDER BY|LIMIT|$)', query, re.IGNORECASE | re.DOTALL)
            field_match = re.findall(r"data\s*->>\s*'([^']+)'", query, re.IGNORECASE)

            col_names = []
            table_names = []
            field_names = []

            if col_match:
                for col_tuple in col_match:
                    col = col_tuple[0] if col_tuple[0] else col_tuple[1]
                    if 'data ->>' not in col:
                        col_names.append(col.strip())

            if table_match:
                raw_tables = re.split(r',\s*', table_match[0].replace('\n', ' ').strip())
                for table in raw_tables:
                    table = re.split(r'\s+(WHERE|GROUP BY|ORDER BY|LIMIT|JOIN)\b', table)[0].strip()
                    table_names.append(table)

            if join_match:
                for join in join_match:
                    table_names.append(join[0].strip())
                    on_clause = join[1]
                    on_cols = re.findall(r'\b(\w+\.\w+)\b', on_clause)
                    col_names.extend(on_cols)

            if where_match:
                where_cols = re.split(r'\s+AND\s+', where_match[0][0].replace('\n', ' ').strip())
                for col in where_cols:
                    match = re.search(r'\b(\w+\.\w+)\b', col)
                    if match:
                        col_names.append(match.group(1))
                        equals_match = re.findall(r'(\w+\.\w+)\s*=\s*(\w+\.\w+)', col)
                        for eq_match in equals_match:
                            col_names.extend(eq_match)

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
            if frequency >= 6 and '*' not in column and 'COUNT(*)' not in column:  
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

"""SELECT COUNT(data ->> 'devEUI')  AS DevEUI
       FROM connecsens.json_montoldre_row
       JOIN connecsens.json_file ON json_montoldre_row.file_id = json_file.id
       WHERE json_file.file_name = 'data20240407.json'""",
    
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
GROUP BY DevEUI ORDER BY DevEUI""",

  """SELECT DISTINCT file_name AS FileNom
    FROM connecsens.json_file 
    JOIN connecsens.json_montoldre_row ON json_montoldre_row.file_id = json_file.id""",

    """SELECT COUNT(data ->> 'devEUI')  AS DevEUI
    FROM connecsens.json_montoldre_row
    JOIN connecsens.json_file ON json_montoldre_row.file_id = json_file.id
    WHERE json_file.file_name = 'data20240407.json'""",

    """SELECT DISTINCT (data ->> 'data-CNSSRFDataTypeName')  AS DateName
    FROM connecsens.json_montoldre_row
    JOIN connecsens.json_file ON json_montoldre_row.(data ->> 'applicationName' ) = json_file.app_name
    WHERE json_file.file_name = 'data20240407.json'""",

"""SELECT DISTINCT (data ->> 'data-CNSSRFDataTypeName')  AS DataName
    FROM connecsens.json_montoldre_row
    JOIN connecsens.json_file ON json_montoldre_row.(data ->> 'applicationName' ) = json_file.app_name""",

"""SELECT date_insert AS InsertedDate
    FROM connecsens.json_file 
    JOIN  connecsens.json_montoldre_row ON json_montoldre_row.file_id = json_file.id
    WHERE json_file.file_name = 'data20240407.json'"""
    
]
    cardinality_csv_path = "C:/Users/spachava/Downloads/Code_Files/Index_Selection/cardinality_file_f.csv"
    main(queries, cardinality_csv_path)
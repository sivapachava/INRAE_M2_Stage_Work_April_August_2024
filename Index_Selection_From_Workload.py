import re
from itertools import combinations
import csv

class WorkloadAnalyzer:
    def __init__(self, queries=None, file_path=None):
        if file_path:
            self.queries = self.read_queries_from_file(file_path)
        else:
            self.queries = queries
        self.columns = []

    def read_queries_from_file(self, file_path):
        with open(file_path, 'r') as file:
            queries = file.read()

            # Remove comments
            queries = re.sub(r'--.*', '', queries)

            # Assuming each query in the file is separated by a semicolon
            queries = queries.split(';')
            queries = [query.strip() for query in queries if query.strip()]

        return queries

    def extract_columns(self):
        query_columns = []
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

                    if 'SUM(' not in col and 'AVG(' not in col and 'MAX(' not in col and 'MIN(' not in col:
                        if 'data ->>' not in col and 'data->>' not in col:
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
                # represents col and index of the current query  within self.queries
                query_columns.append((col, self.queries.index(query)))

            for field in field_names:
                query_columns.append((f"data ->> '{field}'", self.queries.index(query)))

        self.columns = query_columns

        #print(self.columns)
        return self.columns
    

class FrequencyCalculator:
    def __init__(self, columns):
        self.columns = columns

    def calculate_frequency(self):
        frequency_dict = {}
        for col, query_index in self.columns:

            # Create a unique key for each column
            if col not in frequency_dict:
                frequency_dict[col] = {'count': 1, 'queries': [query_index]}
            else:
                frequency_dict[col]['count'] += 1
                frequency_dict[col]['queries'].append(query_index)

        #print(frequency_dict)
        return frequency_dict
    

class CandidateIndexSelector:
    def __init__(self, frequencies):
        self.frequencies = frequencies

    def select_candidate_indices(self):
        candidate_indices = []

        for column, data in self.frequencies.items():
            frequency = data['count']
            queries = data['queries']

            # Select columns that repeat more than number given in condition
            if frequency >= 3 and '*' not in column and 'COUNT(*)' not in column:  
                candidate_indices.append((column, frequency, len(set(queries)))) 

        #print(candidate_indices)
        return candidate_indices
    

class CardinalityChecker:
    def __init__(self, cardinality_csv_path):
        self.cardinality = self._parse_cardinality_csv(cardinality_csv_path)
    
    def _parse_cardinality_csv(self, cardinality_csv_path):
        cardinality = {}

        with open(cardinality_csv_path, newline='', encoding='utf-8') as csvfile: #encoding='utf-8-sig'
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

        for column, frequency, query_count in candidate_indices:
            column_name = column.split(' ->> ')[-1].strip("'")
            cardinality_value = self.cardinality.get(column_name, None)

            if cardinality_value is not None:
                CardCount.append((column, frequency, cardinality_value, query_count))
            else:
                CardCount.append((column, frequency, 'Cardinality not found', query_count))

        #print(CardCount)
        return CardCount
    

class ProcessIndexSelector:
    def __init__(self, counts):
        self.counts = counts

    def select_process_indices(self):
        process_indices = []
        for column, frequency, count, query_count in self.counts:
            if isinstance(count, int) and count >= 3:
                process_indices.append((column, frequency, query_count, count))

        #print(process_indices)
        return process_indices
    

class IndexConfigurationSelector:
    def __init__(self, process_indices):
        self.process_indices = process_indices

    def get_index_configurations(self):
        # Generate all possible index configurations up to the limit we provide
        all_configurations = []
        for r in range(1, 3):
            all_configurations.extend(combinations(self.process_indices, r))

        #print(all_configurations)
        return all_configurations
    

def main(file_path, cardinality_csv_path):
    analyzer = WorkloadAnalyzer(file_path=file_path)
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

    # Print candidate indices with query counts
    for column, frequency, query_count in candidate_indices:
        print(f"{column} is used by {query_count} queries")

    print('\n')
    print('column, frequency, query_count, cardinality')

    # Print configurations
    for config in index_configurations:
        print(tuple((column, frequency, cardinality, query_count) for column, frequency, cardinality, query_count in config))

# File path
file_path = 'Workload2.sql'
cardinality_csv_path = "cardinality_file_f.csv"
main(file_path, cardinality_csv_path)

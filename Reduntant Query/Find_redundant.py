import csv
import re
from collections import Counter


def extract_conditions(query):
    try:
        # Extract conditions between "FROM" and the end of the query using a more comprehensive regular expression
        match = re.search(r'\bFROM\b(.+?)(?:(?:\bGROUP\s+BY\b|\bORDER\s+BY\b|\bHAVING\b|\bLIMIT\b|\bOFFSET\b|\bFETCH\b|\bFOR\b|\bUNION\b|\bINTERSECT\b|\bEXCEPT\b)|$)', query, flags=re.IGNORECASE | re.DOTALL)
        if match:
            conditions = match.group(1).strip().lower()
            # Remove unnecessary spaces
            conditions = ' '.join(conditions.split())
            return conditions
        else:
            return None
    except:
        return None


def find_duplicate_queries(csv_file_path):
    queries = []
    extracted_queries = []
    original_queries = []

    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter='~')
            next(reader)  # Skip header row

            for row in reader:
                try:
                    if row and len(row) > 0:  # Check if the row is not empty and contains at least one element
                        query = row[0]
                        if query.lower().startswith("select"):
                            conditions = extract_conditions(query)
                            if conditions:
                                without_space = conditions.replace(' ', '')
                                original_queries.append(query)
                                extracted_queries.append(conditions)
                                queries.append(without_space)
                except Exception as ex:
                    with open('errors.txt', 'a') as file:
                        file.write(str(ex))


        # extracted text
        with open('extracted_queries.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Select Queries", "Extracted Text"])
            count = len(queries)
            for i in range(count):
                try:
                    writer.writerow([original_queries[i], extracted_queries[i]])
                except:
                    pass

        # Count the occurrences of each query
        query_occurrences = Counter(queries)

        # Filter out queries with more than one occurrence
        duplicate_queries = {query: count for query, count in query_occurrences.items() if count > 1}

        # Write the results to a new CSV file
        with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Original Query", "Extracted Text"])
            for query, count in duplicate_queries.items():
                try:
                    indexes = [index for index, value in enumerate(queries) if value == query]
                    for index in indexes:
                        writer.writerow([original_queries[index], extracted_queries[index]])
                except Exception as ex:
                    with open('errors.txt', 'a') as file:
                        file.write(str(ex))
    except Exception as ex:
        with open('errors.txt', 'a') as file:
            file.write(str(ex))


def main():
    input_file_path = 'input.csv'  # Replace with the path to your input CSV file
    find_duplicate_queries(input_file_path)


main()
import csv


def find_time_taking(csv_file_path):
    queries = []

    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter='~')
            next(reader)  # Skip header row

            for row in reader:
                try:
                    if row and (len(row) > 0) and (int(row[3]) > 1) and (int(row[2]) > 19999):  # Check if the row is not empty and contains at least one element
                        queries.append([row[0], row[1], row[2], row[3]])
                except Exception as ex:
                    with open('errors.txt', 'a') as file:
                        file.write(str(ex))

        # Write the results to a new CSV file
        with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Query", "Inherent", "Average", "Invocation"])
            for query in queries:
                try:
                    writer.writerow(query)
                except Exception as ex:
                    with open('errors.txt', 'a') as file:
                        file.write(str(ex))
    except Exception as ex:
        with open('errors.txt', 'a') as file:
            file.write(str(ex))


def main():
    input_file_path = 'input.csv'  # Replace with the path to your input CSV file
    find_time_taking(input_file_path)


main()
import argparse
import csv

RECORD_IDENTIFIER = "Record Identifier"
TYPE = "Type"
FIELD = "Field"
SOURCE_VALUE = "Source Value"
TARGET_VALUE = "Target Value"

def read_csv(file_path):
    records = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            if not any(reader):  # Check if the file is empty
                raise ValueError("The CSV file is empty.")
            for row in reader:
                records[row[reader.fieldnames[0]]] = row
    except (FileNotFoundError, csv.Error, ValueError) as e:
        print(f"Error reading CSV file {file_path}: {e}")
    return records

def find_missing_records(source_records, target_records):
    missing_in_target = [key for key in source_records if key not in target_records]
    missing_in_source = [key for key in target_records if key not in source_records]
    common_records = set(source_records.keys()).intersection(target_records.keys())
    return missing_in_target, missing_in_source, common_records

def find_discrepancies(source_records, target_records, common_records):
    discrepancies = []
    for key in common_records:
        try:
            source_row = source_records[key]
            target_row = target_records[key]
        except KeyError:
            print(f"KeyError: Record with identifier '{key}' not found in one of the files.")
            continue

        for field in source_row:
            source_value = source_row[field]
            target_value = target_row.get(field, '')

            if source_value != target_value:
                discrepancy = {
                    TYPE: "Field Discrepancy",
                    RECORD_IDENTIFIER: key,
                    FIELD: field,
                    SOURCE_VALUE: source_value,
                    TARGET_VALUE: target_value,
                }
                discrepancies.append(discrepancy)
    return discrepancies

def generate_missing_records(type_label, field_value, missing_keys, discrepancies):
    for key in missing_keys:
        if key != "Expected Output Data":
            discrepancies.append({
                TYPE: type_label,
                RECORD_IDENTIFIER: key,
                FIELD: field_value,
                SOURCE_VALUE: "",
                TARGET_VALUE: "",
            })

def reconcile_csv(source_file, target_file, output_file=None):
    try:
        source_records = read_csv(source_file)
        target_records = read_csv(target_file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except Exception as e:
        print(f"Error reading CSV files: {e}")
        return

    missing_in_target, missing_in_source, common_records = find_missing_records(source_records, target_records)

    discrepancies = []

    generate_missing_records("Missing in Source", "", missing_in_source, discrepancies)
    generate_missing_records("Missing in Target","", missing_in_target, discrepancies)

    discrepancies.extend(find_discrepancies(source_records, target_records, common_records))

    if not source_records or not target_records:
        print("Error: One or both CSV files are empty.")
        return

    if not common_records and not missing_in_target and not missing_in_source:
        print("No records found for reconciliation. Check CSV files.")
        return

    if output_file:
        fieldnames = [TYPE, RECORD_IDENTIFIER, FIELD, SOURCE_VALUE, TARGET_VALUE]
        filtered_discrepancies = [record for record in discrepancies if record[RECORD_IDENTIFIER] != "Expected Output Data"]
        save_report_to_csv(output_file, fieldnames, filtered_discrepancies)


    print("Reconciliation completed:")
    print("Missing in target : ",len(missing_in_target))
    print("Missing in source: ",len(missing_in_source))
def save_report_to_csv(output_file, fieldnames, data):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Report saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="CSV Reconciliation Tool")
    parser.add_argument("-s", "--source", required=True, help="Path to the source CSV file")
    parser.add_argument("-t", "--target", required=True, help="Path to the target CSV file")
    parser.add_argument("-o", "--output", help="Path to save the output reconciliation report")

    args = parser.parse_args()

    reconcile_csv(args.source, args.target, output_file=args.output)

if __name__ == "__main__":
    main()

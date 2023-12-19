import os
import csv
import pytest
from csv_reconciler import read_csv, find_missing_records, find_discrepancies, generate_missing_records, reconcile_csv

# Define test data and paths
TEST_DATA_DIR = "test_data"
SOURCE_CSV = os.path.join(TEST_DATA_DIR, "source.csv")
TARGET_CSV = os.path.join(TEST_DATA_DIR, "target.csv")
OUTPUT_CSV = os.path.join(TEST_DATA_DIR, "output.csv")

# Sample data for testing
source_data = [
    {"Record Identifier": "1", "Field1": "Value1", "Field2": "Value2"},
    {"Record Identifier": "2", "Field1": "Value3", "Field2": "Value4"},
]

target_data = [
    {"Record Identifier": "1", "Field1": "Value1", "Field2": "ModifiedValue2"},
    {"Record Identifier": "3", "Field1": "Value5", "Field2": "Value6"},
]

expected_discrepancies = [
    {"Type": "Field Discrepancy", "Record Identifier": "1", "Field": "Field2", "Source Value": "Value2", "Target Value": "ModifiedValue2"},
    {"Type": "Missing in Target", "Record Identifier": "2", "Field": "", "Source Value": "", "Target Value": ""},
    {"Type": "Missing in Source", "Record Identifier": "3", "Field": "", "Source Value": "", "Target Value": ""},
]

# Create the test data directory and CSV files
@pytest.fixture
def setup_test_data():
    os.makedirs(TEST_DATA_DIR, exist_ok=True)
    with open(SOURCE_CSV, 'w', newline='') as csvfile:
        fieldnames = ["Record Identifier", "Field1", "Field2"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(source_data)

    with open(TARGET_CSV, 'w', newline='') as csvfile:
        fieldnames = ["Record Identifier", "Field1", "Field2"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(target_data)

# Test cases
def test_read_csv(setup_test_data):
    records = read_csv(SOURCE_CSV)
    assert len(records) == 2
    assert "1" in records
    assert "2" in records

def test_find_missing_records(setup_test_data):
    source_records = read_csv(SOURCE_CSV)
    target_records = read_csv(TARGET_CSV)

    missing_in_target, missing_in_source, common_records = find_missing_records(source_records, target_records)

    assert missing_in_target == ["2"]
    assert missing_in_source == ["3"]
    assert common_records == {"1"}

def test_find_discrepancies(setup_test_data):
    source_records = read_csv(SOURCE_CSV)
    target_records = read_csv(TARGET_CSV)

    missing_in_target, missing_in_source, common_records = find_missing_records(source_records, target_records)
    discrepancies = find_discrepancies(source_records, target_records, common_records)

    assert discrepancies == expected_discrepancies


def test_generate_missing_records():
    discrepancies = []
    generate_missing_records("Test Type", "Test Field", ["A", "B"], discrepancies)

    assert len(discrepancies) == 2
    assert discrepancies[0] == {"Type": "Test Type", "Record Identifier": "A", "Field": "Test Field", "Source Value": "", "Target Value": ""}
    assert discrepancies[1] == {"Type": "Test Type", "Record Identifier": "B", "Field": "Test Field", "Source Value": "", "Target Value": ""}

def test_reconcile_csv(setup_test_data, capsys):
    reconcile_csv(SOURCE_CSV, TARGET_CSV, OUTPUT_CSV)

    captured = capsys.readouterr()
    assert "Reconciliation completed:" in captured.out
    assert "Missing in target :" in captured.out
    assert "Missing in source:" in captured.out

    # Check if the output CSV file is created
    assert os.path.isfile(OUTPUT_CSV)

    # Cleanup: Remove the test data directory
    os.remove(SOURCE_CSV)
    os.remove(TARGET_CSV)
    os.remove(OUTPUT_CSV)
    os.rmdir(TEST_DATA_DIR)

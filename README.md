# CLI Documentation: Reconciliation Summarizer
## Overview
The Reconciliation Summarizer CLI app is designed to compare two CSV files and generate an reconciliation report on data missing n the source_file but present in target_file and vice versa and also show any descrepancies in the data between the 2 files. The app reads in two CSV files (termed "source" and
"target"), reconcile the records, and produce a report detailing the differences between the two.

To run the CSV Reconciliation Tool, follow these steps:

# Requirements:
Python installed on your system (version 3.x).
# Steps:
## Download the Script:

Download the csv_reconciliation.py script.
## Install Required Modules:
The script relies on the `argparse` and `csv` modules, which are part of the Python standard library and doesn't require installation.
## Prepare CSV Files:

Prepare the source and target CSV files that you want to reconcile.
## Run the Script:

Open a terminal or command prompt.
Navigate to the directory where the csv_reconciliation.py script is located.

```cd /path/to/directory```

Run the script using the following command:

`python3 csv_reconciliation.py -s path/to/source_file.csv -t path/to/target_file.csv -o path/to/output_file.csv
`


Replace `path/to/source_file.csv`, `path/to/target_file.csv`, and `path/to/output_file.csv` with the actual paths of your source CSV file, target CSV file, and the desired output file for the reconciliation report.

If you don't provide an output file (-o option), the script will print the reconciliation report to the console.

### Example:

`python3 csv_reconciliation.py -s source.csv -t target.csv -o reconciliation_report.csv
`

### Command-line Arguments:
-s or --source: Path to the source CSV file.

-t or --target: Path to the target CSV file.

-o or --output: (Optional) Path to save the output reconciliation report.

## Notes:
If there are any issues during the reconciliation process or if the CSV files are empty, the script will print an error message.

Ensure that you have the necessary read and write permissions for the specified files and directories.

The reconciliation report includes information about missing records in the source and target files, as well as discrepancies in field values between common records.

Now you should be able to run the CSV Reconciliation Tool successfully. Adjust the file paths and options according to your specific use case.
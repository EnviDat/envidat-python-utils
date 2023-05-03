# Script to update variable number of EnviDat records on DataCite.
# Record names are entered as space separated values after
# the --records argument
# Example command to run script:
# python -m scripts.datacite_updater_records --records test-dataset supertest

# Imports
import argparse
import time

from envidat.doi.datacite_updater import datacite_update_records

# Assign start_time
print("Starting datacite_updater_records.py....")
start_time = time.time()

# Create the parser
parser = argparse.ArgumentParser()

# Add records argument
parser.add_argument(
    "--records", type=str, nargs="+", required=True, help="EnviDat record 'name' values"
)
args = parser.parse_args()

# Get record_names from args
record_names = args.records

# Update EnviDat records on DataCite
print("See log for individual record updates")
datacite_update_records(record_names)

# Assign and format timer, print execution time
end_time = time.time()
timer = end_time - start_time
print(f"Ending datacite_updater_records.py, that took {round(timer, 2)} seconds")

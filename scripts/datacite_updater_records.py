import time
import argparse

from envidat.doi.datacite_updater import datacite_update_all_records

# COMMAND to run script:   python -m scripts.datacite_updater_records

# Create the parser
parser = argparse.ArgumentParser()

# Add records argument
parser.add_argument('--records', type=str, nargs='+', required=True, help="EnviDat record 'name' values")
args = parser.parse_args()

# TODO finish script
print(args.records)

# Assign start_time
print("Starting datacite_updater_records.py....")
start_time = time.time()

# Update EnviDat records on DataCite
print("See log for individual record updates")
# datacite_update_all_records()

# Assign and format timer, print execution time
end_time = time.time()
timer = end_time - start_time
print(f"Ending datacite_updater_records.py, that took {round(timer, 3)} seconds")

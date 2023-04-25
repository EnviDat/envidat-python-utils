
import time

from envidat.doi.datacite_updater import datacite_update_all_records

# COMMAND to run script:   python -m scripts.datacite_importer_all_records

# Assign start_time
print("Starting datacite_updater_all_records.py....")
start_time = time.time()

# Update all EnviDat records on DataCite
print("See log for individual record updates")
datacite_update_all_records()

# Assign and format timer, print execution time
end_time = time.time()
timer = end_time - start_time
print(f"Ending datacite_updater_all_records.py, that took {round(timer, 3)} seconds")



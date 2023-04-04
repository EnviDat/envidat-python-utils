
import time

from envidat.doi.datacite_updater import datacite_create_and_update_all_records

# COMMAND to run script:   python -m scripts.datacite_importer

# Assign start_time
print("Starting datacite_importer.py....")
start_time = time.time()

# Create and update all EnviDat records on DataCite
print("See 'datacite_importer.log' for logs of individual record creation/update")
datacite_create_and_update_all_records()

# Assign and format timer, print execution time
end_time = time.time()
timer = end_time - start_time
print(f"Ending datacite_importer.py, that took {round(timer, 3)} seconds")




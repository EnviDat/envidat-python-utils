
from envidat.metadata import Record
from envidat.api.v1 import get_package

test_package = get_package('number_of_forest_plots-125')
record1 = Record(input_data=test_package, extract='iso')

# result_iso = record1.to_iso()
# print(result_iso)

result_ris = record1.to_ris()
print(result_ris)

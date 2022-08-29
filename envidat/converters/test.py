
from envidat.metadata import Record
from envidat.api.v1 import get_package

test_package = get_package('number_of_forest_plots-125')
record1 = Record(input_data=test_package, extract='iso')

test_package_2 = get_package('seilaplan-tutorial-dhm-kacheln-zusammenfugen')
record2 = Record(input_data=test_package_2)

# result_iso = record1.to_iso()
# print(result_iso)

# result_ris = record1.to_ris()
# print(result_ris)

# result_bibtex = record1.to_bibtex()
# print(result_bibtex)

# result_dif = record1.to_dif()
# print(result_dif)

# result_dif_2 = record2.to_dif()
# print(result_dif_2)

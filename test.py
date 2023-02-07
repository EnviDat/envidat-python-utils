# import logging
# from envidat.s3.bucket import Bucket
# from envidat.utils import load_dotenv_if_in_debug_mode, get_logger
# get_logger()
# log = logging.getLogger(__name__)
# load_dotenv_if_in_debug_mode(".env.secret")
# # new_bucket = Bucket("frontend-dev", is_new=True, is_public=True)
# # new_bucket.configure_static_website()
# # new_bucket = Bucket("envidat-staging")
# # new_bucket.set_cors_config(allow_all=True)
# # log.warning(new_bucket.get_cors_config())
# # new_bucket = Bucket("frontend-static")
# # new_bucket.upload_dir("static", contents_only=True)
# from envidat.converters.iso_converter import iso_convert_dataset
#
# test iso = iso_convert_dataset()
# from envidat.converters.datacite_converter import datacite_convert_dataset
# record.to_datacite()
import json

# from tests.conftest import datacite_converter_one_package
# from tests.test_converters import get_datacite_converters_one_package
# get_datacite_converters_one_package()
# datacite_convert_dataset()


from envidat.api.v1 import get_package
from envidat.metadata import Record
from xmltodict import parse

# package_name = "metadata-quality-and-logistics-the-fair-data-publication-workflow-at-eawag-and"
# host = "https://envidat04.wsl.ch/"
# package = get_package(package_name, host)


# TEST PACKAGES

# package_name = "distribution-maps-of-permanent-grassland-habitats-for-switzerland"
# package_name = "observed-and-simulated-snow-profile-data-from-switzerland"

# DORA PID has no DOI  for this package
# package_name = "accessibility-of-the-swiss-forest-for-economic-wood-extraction"

# Use this package for testing extracting DOIs from related_datasets
# package_name = "ozone-measurement-and-analysis-in-the-intercantonal-forest-observation-progra"

# package_name = "chelsa-climatologies"
package_name = "accessibility-of-the-swiss-forest-for-economic-wood-extraction"
# package_name = "survey-energy-transition-municipal-level-switzerland"

# TODO check this package to validate DORA links WITHOUT DOIS
# package_name = "survey-energy-transition-municipal-level-switzerland"

package = get_package(package_name)

record = Record(package, "datacite")

result = record.get_content()
# print('\n\n')
print(result)

# json_result = parse(result)
# # print(json_result)
#
# json_obj = json.dumps(json_result)
#
#
# with open("sample.json", "w") as outfile:
#     outfile.write(json_obj)

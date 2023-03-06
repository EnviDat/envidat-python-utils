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

from envidat.doi.datacite_publisher import xml_to_base64, publish_datacite
from xmltodict import parse

from envidat.api.v1 import get_package
from envidat.metadata import Record, get_all_metadata_record_list


with open("test.json", encoding="utf-8") as test_json:
    test_package = json.load(test_json)

# from tests.conftest import datacite_converter_one_package
# from tests.test_converters import get_datacite_converters_one_package
# get_datacite_converters_one_package()
# datacite_convert_dataset()


# package_name = "metadata-quality-and-logistics-the-fair-data-publication-workflow-at-eawag-and"
# host = "https://envidat04.wsl.ch/"
# package = get_package(package_name, host)


# TEST PACKAGES

# package_name = "distribution-maps-of-permanent-grassland-habitats-for-switzerland"
# package_name = "observed-and-simulated-snow-profile-data-from-switzerland"

# Used for testing DORA
# package_name = "wml_bilderstudie"
# package_name = "hydropot_integral"

# DORA PID has no DOI  for this package
# package_name = "accessibility-of-the-swiss-forest-for-economic-wood-extraction"

# Use this package for testing extracting DOIs from related_datasets
# package_name = "ozone-measurement-and-analysis-in-the-intercantonal-forest-observation-progra"

# TODO check this package to validate DORA links WITHOUT DOIS
# package_name = "survey-energy-transition-municipal-level-switzerland"

# package_name = "chelsa-climatologies"
# package_name = "satellite-avalanche-mapping-validation"
# package_name = "survey-energy-transition-municipal-level-switzerland"
# package_name = "arthropod-biomass-abundance-species-richness-trends-limpach"

# Used for testing "sizes"
# package_name = "multifaceted-diversity-alps"

# Used for testing "rightsList" and multiple author "affiliation" values
# package_name = "satellite-avalanche-mapping-validation"
# package_name = "pfynwaldgasexchange"
# package_name = "nacl_interfacial_phasechanges"
# package_name = "soil-water-measurements-wdb"
# package_name = "lidar-davos-wolfgang"

# Used for testing restricted resources
# package_name = "stable-water-isotopes-in-snow-and-vapor-on-the-weissfluhjoch"

# Used for testing "geoLocations"
# package_name = "envidat-lwf-51"  # Multipoint
# package_name = "als-based-snow-depth"   # Point

# Used for testing "fundingReferences"
# package_name = "distributed-subcanopy-datasets"   # grant_number

# Used for testing "contributor" tag with "affiliation"
# package_name = "the-origin"

# Used for testing conrtibutor without "affiliation"
# package_name = "multifaceted-diversity-alps"

# Used for testing datasets without DOIs
package_name = "sediment-transport-observations-in-swiss-mountain-streams"
# doi = "10.16904/test6"

# DOI in draft state
# doi = "10.16904/6s7f-am07"


# TEST package used for dev
# package_name = "accessibility-of-the-swiss-forest-for-economic-wood-extraction"
# doi = "10.16904/envidat.363"

# package = get_package(package_name)

# result = reserve_draft_doi_datacite(package)

doi = "10.16904/test6"
result = publish_datacite(doi, test_package)

# result = publish_datacite(doi, package)
# result = publish_datacite(doi, package, is_update=True)
print(result)

# record = Record(package, "datacite")
#
# result = record.get_content()
# print(type(result))
# print(result)
#
# print('\n\n')
#
# xml = xml_to_base64(result)
# print(xml)



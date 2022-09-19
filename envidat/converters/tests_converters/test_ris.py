"""Test ris_converter.py output by comparing it to CKAN API produced RIS output."""

from envidat.api.v1 import get_package, get_metadata_list_with_resources
from envidat.converters.ris_converter import ris_convert_dataset
from envidat.converters.tests_converters.ckan_converters_endpoints import get_ris_ckan_endpoint
from envidat.utils import get_url


def test_ris_converters_one_package(package_name='seilaplan-tutorial-dhm-kacheln-zusammenfugen'):

    package = get_package(package_name)

    ris_ckan_endpoint = get_ris_ckan_endpoint(package)
    request = get_url(ris_ckan_endpoint)
    ckan_output = request.text

    converter_output = ris_convert_dataset(package)

    assert (
        ckan_output == converter_output,
        f'Package with name {package_name} RIS CKAN output does not equal ris_converter_dataset() output'
    )


def test_ris_converters_all_packages():

    packages = get_metadata_list_with_resources()
    ckan_ris_packages = []
    converter_ris_packages = []

    for package in packages:

        ris_ckan_endpoint = get_ris_ckan_endpoint(package)
        request = get_url(ris_ckan_endpoint)
        ckan_output = request.text
        ckan_ris_packages.append(ckan_output)

        converter_output = ris_convert_dataset(package)
        converter_ris_packages.append(converter_output)

    assert (
        ckan_ris_packages == converter_ris_packages,
        f'RIS CKAN output does not equal ris_converter_dataset() output'
    )

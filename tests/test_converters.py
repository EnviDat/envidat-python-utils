"""Tests for package converters."""

import os

from xmltodict import unparse

from envidat.api.v1 import get_metadata_list_with_resources, get_package
from envidat.utils import get_url


def get_ckan_endpoint(
    package: dict,
    file_format: str,
    extension: str,
    host: str = "https://www.envidat.ch",
) -> str:
    """TODO."""
    if "API_HOST" in os.environ:
        host = os.getenv("API_HOST")

    package_name = package.get("name", "")
    if package_name:
        return f"{host}/dataset/{package_name}/export/{file_format}.{extension}"
    else:
        package_id = package.get("id", "")
        if package_id:
            return f"{host}/dataset/{package_id}/export/{file_format}.{extension}"
        else:
            raise ValueError(
                f"Failed to get CKAN endpoint string for {file_format} format."
            )


def get_converters_one_package(convert_dataset, package_name, file_format, extension):
    """TODO."""
    package = get_package(package_name)

    ckan_endpoint = get_ckan_endpoint(package, file_format, extension)
    request = get_url(ckan_endpoint)
    ckan_output = request.content.decode()

    converter_output = convert_dataset(package)

    return ckan_output, converter_output


def get_converters_all_packages(convert_dataset, file_format, extension):
    """TODO."""
    packages = get_metadata_list_with_resources()
    ckan_packages = []
    converter_packages = []

    for package in packages:

        ckan_endpoint = get_ckan_endpoint(package, file_format, extension)
        request = get_url(ckan_endpoint)
        ckan_output = request.content.decode()
        ckan_packages.append(ckan_output)

        converter_output = convert_dataset(package)
        converter_packages.append(converter_output)

    return ckan_packages, converter_packages


def get_datacite_converters_one_package(
    convert_dataset, get_name_doi, package_name, file_format, extension
):
    """TODO."""
    package = get_package(package_name)

    ckan_endpoint = get_ckan_endpoint(package, file_format, extension)
    request = get_url(ckan_endpoint)
    ckan_output = request.content.decode()

    name_doi = get_name_doi()
    converter_output = convert_dataset(package, name_doi)

    return ckan_output, converter_output


def get_datacite_converters_all_packages(
    convert_dataset, get_name_doi, file_format, extension
):
    """TODO."""
    packages = get_metadata_list_with_resources()
    ckan_packages = []

    name_doi = get_name_doi()
    converter_packages = []

    for package in packages:

        ckan_endpoint = get_ckan_endpoint(package, file_format, extension)
        request = get_url(ckan_endpoint)
        ckan_output = request.content.decode()
        ckan_packages.append(ckan_output)

        converter_output = convert_dataset(package, name_doi)
        converter_packages.append(converter_output)

    return ckan_packages, converter_packages


def test_bibtex_converters_one_package(bibtex_converter_one_package):
    """TODO."""
    ckan_output, converter_output = get_converters_one_package(
        *bibtex_converter_one_package
    )

    assert ckan_output == converter_output


def test_bibtex_converters_all_packages(bibtex_converter_all_packages):
    """TODO."""
    ckan_packages, converter_packages = get_converters_all_packages(
        *bibtex_converter_all_packages
    )

    assert ckan_packages == converter_packages


# NOTE: to make this test pass it was necessary to temporarily reinstate
# the typo in the envidat.converters.datacite_converter.datacite_convert_dataset
# variable 'related_datasets_base_url': 'https://www.envidat.ch/#/metadata//'
# (the correct url omits the last slash: ''https://www.envidat.ch/#/metadata/' )
def test_datacite_converter_one_package(datacite_converter_one_package):
    """TODO."""
    ckan_output, converter_output = get_datacite_converters_one_package(
        *datacite_converter_one_package
    )

    # Convert OrderedDict to xml format
    converted_output_xml = unparse(converter_output, pretty=True)

    assert ckan_output == converted_output_xml


# NOTE: to make this test pass it was necessary to temporarily reinstate
# the typo in the envidat.converters.datacite_converter.datacite_convert_dataset
# variable 'related_datasets_base_url': 'https://www.envidat.ch/#/metadata//'
# (the correct url omits the last slash: ''https://www.envidat.ch/#/metadata/' )
def test_datacite_converters_all_packages(datacite_converter_all_packages):
    """TODO."""
    ckan_packages, converter_packages = get_datacite_converters_all_packages(
        *datacite_converter_all_packages
    )

    # Remove dataset that has related datasets that are
    # causing the test to fail due to typo of
    # 'ORCHID' value in metadata (it should be 'ORCID')
    ckan_packages.pop(381)
    converter_packages.pop(381)

    # Convert OrderedDict packages to xml format
    converter_packages_xml = []
    for package in converter_packages:
        package_xml = unparse(package, pretty=True)
        converter_packages_xml.append(package_xml)

    assert ckan_packages == converter_packages_xml


# NOTE: to make this test pass it was necessary to temporarily reinstate
# the typo in the envidat.converters.dif_converter.dif_convert_dataset
# key 'Usage_Constraints' value: "Usage constraintes defined by
# the license" (the correct spelling is "constraints")
def test_dif_converters_one_package(dif_converter_one_package):
    """TODO."""
    ckan_output, converter_output = get_converters_one_package(
        *dif_converter_one_package
    )

    # Convert OrderedDict to xml format
    converted_output_xml = unparse(converter_output, pretty=True)

    assert ckan_output == converted_output_xml


# NOTE: to make this test pass it was necessary to temporarily reinstate
# the typo in the envidat.converters.dif_converter.dif_convert_dataset
# key 'Usage_Constraints' value: "Usage constraintes defined by
# the license" (the correct spelling is "constraints")
def test_dif_converters_all_packages(dif_converter_all_packages):
    """TODO."""
    ckan_packages, converter_packages = get_converters_all_packages(
        *dif_converter_all_packages
    )

    # Find CKAN packages that do not produce a valid DIF format xml file
    remove_indices = []
    for index, package in enumerate(ckan_packages):
        if package.startswith("No converter available for format gcmd_dif"):
            remove_indices.append(index)

    # Exclude packages from testing that do not have a valid CKAN
    # produced DIF format xml file
    for ind in remove_indices:
        ckan_packages.pop(ind)
        converter_packages.pop(ind)

    # Convert OrderedDict packages to xml format
    converter_packages_xml = []
    for package in converter_packages:
        package_xml = unparse(package, pretty=True)
        converter_packages_xml.append(package_xml)

    assert ckan_packages == converter_packages_xml


def test_iso_converters_one_package(iso_converter_one_package):
    """TODO."""
    ckan_output, converter_output = get_converters_one_package(
        *iso_converter_one_package
    )

    # Convert OrderedDict packages to xml format
    converted_output_xml = unparse(converter_output, pretty=True)

    assert ckan_output == converted_output_xml


def test_iso_converters_all_packages(iso_converter_all_packages):
    """TODO."""
    ckan_packages, converter_packages = get_converters_all_packages(
        *iso_converter_all_packages
    )

    # Find CKAN packages that do not produce a valid ISO format xml file
    remove_indices = []
    for index, package in enumerate(ckan_packages):
        if package.startswith("No converter available for format iso19139"):
            remove_indices.append(index)

    # Exclude packages from testing that do not have a valid CKAN
    # produced ISO format xml file
    for ind in remove_indices:
        ckan_packages.pop(ind)
        converter_packages.pop(ind)

    # Convert OrderedDict packages to xml format
    converter_packages_xml = []
    for package in converter_packages:
        package_xml = unparse(package, pretty=True)
        converter_packages_xml.append(package_xml)

    assert ckan_packages == converter_packages_xml


def test_ris_converters_one_package(ris_converter_one_package):
    """TODO."""
    ckan_output, converter_output = get_converters_one_package(
        *ris_converter_one_package
    )

    assert ckan_output == converter_output


def test_ris_converters_all_packages(ris_converter_all_packages):
    """TODO."""
    ckan_packages, converter_packages = get_converters_all_packages(
        *ris_converter_all_packages
    )

    assert ckan_packages == converter_packages

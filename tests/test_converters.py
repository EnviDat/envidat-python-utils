
import os

from envidat.api.v1 import get_package, get_metadata_list_with_resources
from envidat.utils import get_url

from xmltodict import unparse


def get_ckan_endpoint(
        package: dict,
        file_format: str,
        extension: str,
        host: str = 'https://www.envidat.ch'
) -> str:

    if "API_HOST" in os.environ:
        host = os.getenv("API_HOST")

    package_name = package.get('name', '')
    if package_name:
        return f'{host}/dataset/{package_name}/export/{file_format}.{extension}'
    else:
        package_id = package.get('id', '')
        if package_id:
            return f'{host}/dataset/{package_id}/export/{file_format}.{extension}'
        else:
            raise ValueError(f'Failed to get CKAN endpoint string for {file_format} format.')


def get_converters_one_package(
        convert_dataset,
        package_name,
        file_format,
        extension
):

    package = get_package(package_name)

    ckan_endpoint = get_ckan_endpoint(package, file_format, extension)
    request = get_url(ckan_endpoint)
    ckan_output = request.content.decode()

    converter_output = convert_dataset(package)

    return ckan_output, converter_output


def get_converters_all_packages(
        convert_dataset,
        file_format,
        extension
):

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


def test_bibtex_converters_one_package(bibtex_converter_one_package):

    ckan_output, converter_output = get_converters_one_package(*bibtex_converter_one_package)

    assert ckan_output == converter_output


def test_bibtex_converters_all_packages(bibtex_converter_all_packages):

    ckan_packages, converter_packages = get_converters_all_packages(*bibtex_converter_all_packages)

    assert ckan_packages == converter_packages


def test_iso_converters_one_package(iso_converter_one_package):

    ckan_output, converter_output = get_converters_one_package(*iso_converter_one_package)

    # Convert OrderedDict to xml format
    converted_output_xml = unparse(converter_output, pretty=True)

    # print(type(ckan_output))
    # print(len(ckan_output))
    # print(ckan_output)
    # print('\n')
    #
    # print(type(converted_output_xml))
    # print(len(converted_output_xml))
    # print(converted_output_xml)

    assert ckan_output == converted_output_xml


def test_iso_converters_all_packages(iso_converter_all_packages):

    ckan_packages, converter_packages = get_converters_all_packages(*iso_converter_all_packages)

    # Convert OrderedDict to xml format
    converter_packages_xml = []
    for package in converter_packages:
        package_xml = unparse(package, pretty=True)
        converter_packages_xml.append(package_xml)

    # print(type(ckan_packages))
    # print(len(ckan_packages))
    # print(ckan_packages[67])
    # print('\n')
    #
    # print(type(converter_packages_xml))
    # print(len(converter_packages_xml))
    # print(converter_packages_xml[67])

    assert ckan_packages == converter_packages_xml


def test_ris_converters_one_package(ris_converter_one_package):

    ckan_output, converter_output = get_converters_one_package(*ris_converter_one_package)

    assert ckan_output == converter_output


def test_ris_converters_all_packages(ris_converter_all_packages):

    ckan_packages, converter_packages = get_converters_all_packages(*ris_converter_all_packages)

    assert ckan_packages == converter_packages


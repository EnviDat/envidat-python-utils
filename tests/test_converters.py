
import os

from envidat.api.v1 import get_package, get_metadata_list_with_resources
from envidat.utils import get_url


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


def test_ris_converters_one_package(ris_converter_one_package):

    ckan_output, converter_output = get_converters_one_package(*ris_converter_one_package)

    assert (
        ckan_output == converter_output,
        f'FAILED TEST comparing one package: RIS CKAN output does not equal ris_converter_dataset() output'
    )


def test_ris_converters_all_packages(ris_converter_all_packages):

    ckan_packages, converter_packages = get_converters_all_packages(*ris_converter_all_packages)

    assert (
        ckan_packages == converter_packages,
        f'FAILED TEST comparing all packages: RIS CKAN output does not equal ris_converter_dataset() output'
    )

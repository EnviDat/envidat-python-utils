"""V1 CKAN based API."""

import logging
import os

from envidat.utils import get_url

log = logging.getLogger(__name__)


def get_metadata_list(
        host: str = "https://www.envidat.ch", sort_result: bool = None
) -> list:
    """Get package/metadata list from API.

    Host url as a parameter or from environment.

    Args:
        host (str): API host url. Attempts to get from environment if omitted.
            Defaults to https://www.envidat.ch.
        sort_result (bool): Sort result alphabetically by metadata name.
            Default to None.

    Returns:
        list: List of JSON formatted packages.
    """
    if "API_HOST" in os.environ:
        log.debug("Getting API host from environment variable.")
        host = os.getenv("API_HOST")

    log.info(f"Getting package list from {host}.")
    try:
        package_names = get_url(f"{host}/api/3/action/package_list").json()
    except AttributeError as e:
        log.error(e)
        log.error(f"Getting package names from API failed. Returned: {package_names}")
        raise AttributeError("Failed to extract package names as JSON.")

    log.debug("Extracting [result] key from JSON.")
    package_names = list(package_names["result"])

    log.info(f"Returned {len(package_names)} metadata entries from API.")

    if sort_result:
        log.debug("Sorting return alphabetically.")
        package_names = sorted(package_names, reverse=False)

    return package_names


def get_metadata_json_with_resources(
        host: str = "https://www.envidat.ch",
        path: str = "/api/3/action/current_package_list_with_resources?limit=100000"
) -> str:
    """Get package/metadata as string in JSON format with associated resources from API.

    Host url as a parameter or from environment.

    Args:
        host (str): API host url. Attempts to get from environment if omitted.
            Defaults to https://www.envidat.ch.
        path (str): API host path. Attempts to get from environment if omitted.
            Defaults to /api/3/action/current_package_list_with_resources?limit=100000

    Note:
        Limits results to 100000, otherwise returns only 10 results.

    Returns:
        string:  String of JSON formatted packages, with nested resources.
    """
    if "API_HOST" in os.environ and "API_PATH" in os.environ:
        log.debug("Getting API host and path from environment variables.")
        host = os.getenv("API_HOST")
        path = os.getenv("API_PATH")

    log.info(f"Getting package list with resources from {host}.")
    try:
        package_names_with_resources = get_url(f"{host}/{path}").json()
    except AttributeError as e:
        log.error(e)
        log.error(
            "Getting package names with resources from API failed. "
        )
        raise AttributeError("Failed to extract package names as JSON.")

    return package_names_with_resources


def get_metadata_list_with_resources(
        sort_result: bool = None
) -> list:
    """Get package/metadata as list of results with associated resources from API.

    Args:
        sort_result (bool): Sort result alphabetically by metadata name.
            Default to None.

    Note:
        Limits results to 100000, otherwise returns only 10 results.

    Returns:
        list: List of JSON formatted packages, with nested resources.
    """

    # Get package/metadata as string in JSON format with associated resources from API
    package_names_with_resources = get_metadata_json_with_resources()

    # Extract results and assign them to a list
    log.debug("Extracting [result] key from JSON.")
    package_names_with_resources = list(package_names_with_resources["result"])
    log.info(f"Returned {len(package_names_with_resources)} metadata entries from API.")

    # If sort_result true sort by name key alpahebetically
    if sort_result:
        log.debug("Sorting return by nested 'name' key alphabetically.")
        package_names_with_resources = sorted(
            package_names_with_resources, key=lambda x: x["name"], reverse=False
        )

    return package_names_with_resources

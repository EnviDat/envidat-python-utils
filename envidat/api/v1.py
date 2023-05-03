"""V1 CKAN based API."""

# TODO update documentation of functions in GitLab
# TODO test functions to make sure they can read environment variables

import logging
import os

from envidat.utils import get_url, get_url_response, load_dotenv_if_in_debug_mode

log = logging.getLogger(__name__)

# Load config from environment variables
load_dotenv_if_in_debug_mode(".env")


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
        log.error("Getting package names from API failed.")
        raise AttributeError("Failed to extract package names as JSON.")

    log.debug("Extracting [result] key from JSON.")
    package_names = list(package_names["result"])

    log.info(f"Returned {len(package_names)} metadata entries from API.")

    if sort_result:
        log.debug("Sorting return alphabetically.")
        package_names = sorted(package_names, reverse=False)

    return package_names


def get_protocol_and_domain(
    protocol: str = "https", domain: str = "www.envidat.ch"
) -> tuple[str, str]:
    """Extract protocol string and domain string from API host.

    Args:
        protocol (str): API host protocol. Attempts to get from environment if omitted.
            Defaults to https
        domain (str): API host domain. Attempts to get from environment if omitted.
            Defaults to www.envidat.ch

    Returns:
        tuple (<str: protocol>, <str: domain>): Protocol and domain from API host.
    """
    if "API_HOST" in os.environ:
        host = os.getenv("API_HOST")
        protocol = host.partition("://")[0]
        domain = host.partition("://")[2]
        return protocol, domain

    return protocol, domain


def get_package(
    package_name: str,
    host: str = "https://www.envidat.ch",
    path: str = "/api/action/package_show?id=",
) -> dict:
    """Get individual package (metadata entry) as dictionary from API.

    Args:
        package_name (str): API package 'name' or 'id' value.
        host (str): API host url. Attempts to get from environment if omitted.
            Defaults to "https://www.envidat.ch"
        path (str): API host path. Attempts to get from environment if omitted.
            Defaults to "api/action/package_show?id="

    Returns:
        dict: Dictionary of package (metadata entry).
    """
    if "API_HOST" in os.environ and "API_PACKAGE_SHOW" in os.environ:
        log.debug("Getting API host and path from environment variables.")
        host = os.getenv("API_HOST")
        path = os.getenv("API_PACKAGE_SHOW")

    log.info(f"Getting package from {host}.")
    try:
        # Extract result dictionary from API call
        json_data = get_url(f"{host}{path}{package_name}").json()
        package = json_data["result"]
    except AttributeError as e:
        log.error(e)
        log.error("Getting package from API failed.")
        raise AttributeError("Failed to extract package as JSON.")

    return package


# TODO refactor this or get_package() as they have similar functionality,
#  check usage of functions in project
def get_envidat_record(
    package_name: str,
    host: str = "https://www.envidat.ch",
    path: str = "/api/action/package_show?id=",
    cookie: str | None = None,
) -> dict | None:
    """Get individual EnviDat record (metadata entry) as dictionary from API.

    Args:
        package_name (str): API package 'name' or 'id' value.
        host (str): API host url. Attempts to get from environment if omitted.
            Defaults to "https://www.envidat.ch"
        path (str): API host path. Attempts to get from environment if omitted.
            Defaults to "api/action/package_show?id="
        cookie (str | None): Cookie passed to API call in header,
                             default value is None as this argument is not
                             always used

    Returns:
        dict: Dictionary of package (metadata entry).
    """
    # Extract environment variables from config needed to call CKAN
    # If environment variables cannot be extracted then use default values
    # for host and path
    try:
        host = os.environ("API_HOST")
        path = os.environ("API_PACKAGE_SHOW")
    except KeyError as e:
        log.error(f"KeyError: {e} does not exist in environment vars")
    except AttributeError as e:
        log.error(e)

    try:
        # Extract result dictionary from API call, pass cookie if is truthy
        if cookie:
            response = get_url_response(f"{host}{path}{package_name}", cookie=cookie)
        else:
            response = get_url_response(f"{host}{path}{package_name}")

        # TODO improve error handling
        # Handle HTTPError from API call
        if response.status_code != 200:
            return {"status_code": response.status_code, "result": response.content}

        # Return package (derived from "result" key in response)
        if response:
            data = response.json()
            package = data["result"]
            return {"status_code": response.status_code, "result": package}

        # TODO handle if response is None

    except AttributeError as e:
        log.error(e)
        return {
            "status_code": 500,
            "result": "Failed to extract package as JSON from API, check logs",
        }


def get_metadata_json_with_resources(
    host: str = "https://www.envidat.ch",
    path: str = "/api/3/action/current_package_list_with_resources?limit=100000",
) -> dict:
    """Get all current package/metadata as dictionary with associated resources from
    API.

    Args:
        host (str): API host url. Attempts to get from environment if omitted.
            Defaults to https://www.envidat.ch
        path (str): API host path. Attempts to get from environment if omitted.
            Defaults to /api/3/action/current_package_list_with_resources?limit=100000

    Note:
        Limits results to 100000, otherwise returns only 10 results.

    Returns:
        dict:  Dictionary of packages, with nested resources.
    """
    if (
        "API_HOST" in os.environ
        and "API_PATH_CURRENT_PACKAGE_LIST_WITH_RESOURCES" in os.environ
    ):
        log.debug("Getting API host and path from environment variables.")
        host = os.getenv("API_HOST")
        path = os.getenv("API_PATH_CURRENT_PACKAGE_LIST_WITH_RESOURCES")

    log.info(f"Getting package list with resources from {host}.")
    try:
        package_names_with_resources = get_url(f"{host}{path}").json()
    except AttributeError as e:
        log.error(e)
        log.error("Getting package names with resources from API failed.")
        raise AttributeError("Failed to extract package names as JSON.")

    return package_names_with_resources


def get_metadata_list_with_resources(sort_result: bool = None) -> list:
    """Get all current package/metadata as list of results with associated resources.

    Args:
        sort_result (bool): Sort result alphabetically by metadata name.
            Default to None.

    Note:
        Limits results to 100000, otherwise returns only 10 results.

    Returns:
        list: List of packages, with nested resources.
    """
    # Get package/metadata as string in JSON format with associated resources from API
    package_names_with_resources = get_metadata_json_with_resources()

    # Extract results and assign them to a list
    log.debug("Extracting [result] key from JSON.")
    package_names_with_resources = list(package_names_with_resources["result"])
    log.info(f"Returned {len(package_names_with_resources)} metadata entries from API.")

    # If sort_result true sort by name key alphabetically
    if sort_result:
        log.debug("Sorting return by nested 'name' key alphabetically.")
        package_names_with_resources = sorted(
            package_names_with_resources, key=lambda x: x["name"], reverse=False
        )

    return package_names_with_resources


def get_metadata_name_doi() -> dict:
    """Get all current package/metadata names and DOIs as a dictionary.

    Note:
        Packages that do not have DOIs are assigned a default value
        of an empty string ''.

    Returns:
        dict: Dictionary of package information with names as keys
        and associated DOIs as values.
    """
    all_packages = get_metadata_list_with_resources()
    return {package.get("name"): package.get("doi", "") for package in all_packages}

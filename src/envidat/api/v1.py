import os
import logging
import requests


log = logging.getLogger(__name__)


def _get_url(url: str) -> requests.Response:
    "Helper wrapper to get a URL with additional error handling."

    try:
        log.debug(f"Attempting to get {url}")
        r = requests.get(url)
        r.raise_for_status()
        return r
    except requests.exceptions.ConnectionError as e:
        log.error(f"Could not connect to internet on get: {r.request.url}")
        log.error(e)
    except requests.exceptions.HTTPError as e:
        log.error(f"HTTP response error on get: {r.request.url}")
        log.error(e)
    except requests.exceptions.RequestException as e:
        log.error(f"Request error on get: {r.request.url}")
        log.error(f"Request: {e.request}")
        log.error(f"Response: {e.response}")
    except Exception as e:
        log.error(e)
        log.error(f"Unhandled exception occured on get: {r.request.url}")

    return None


def get_metadata_list(host: str = None, sort_result: bool = None) -> list:
    """
    Get package/metadata list from API.
    Host url as a parameter or from environment.

    :param host: API host url. Attempts to get from environment if omitted.
    :param sort_result: Sort result alphabetically by metadata name.
    """

    if host is None:
        log.debug("No API host specified, getting from environment.")
        host = os.getenv("API_HOST", default="https://www.envidat.ch")

    log.info(f"Getting package list from {host}.")
    try:
        package_names = _get_url(f"{host}/api/3/action/package_list").json()
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


def get_metadata_list_with_resources(
    host: str = None, sort_result: bool = None
) -> list:
    """
    Get package/metadata list with associated resources from API.
    Host url as a parameter or from environment.

    :param host: API host url. Attempts to get from environment if omitted.
    :param sort_result: Sort result alphabetically by metadata name.

    Note: uses limit 100000, otherwise returns only 10 results.
    """

    if host is None:
        log.debug("No API host specified, getting from environment.")
        host = os.getenv("API_HOST", default="https://www.envidat.ch")

    log.info(f"Getting package list with resources from {host}.")
    try:
        package_names_with_resources = _get_url(
            f"{host}/api/3/action/current_package_list_with_resources?limit=100000"
        ).json()
    except AttributeError as e:
        log.error(e)
        log.error(
            "Getting package names with resources from API failed. "
            f"Returned: {package_names_with_resources}"
        )
        raise AttributeError("Failed to extract package names as JSON.")

    log.debug("Extracting [result] key from JSON.")
    package_names_with_resources = list(package_names_with_resources["result"])

    log.info(f"Returned {len(package_names_with_resources)} metadata entries from API.")

    if sort_result:
        log.debug("Sorting return by nested 'name' key alphabetically.")
        package_names_with_resources = sorted(
            package_names_with_resources, key=lambda x: x["name"], reverse=False
        )

    return package_names_with_resources

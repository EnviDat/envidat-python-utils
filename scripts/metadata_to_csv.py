'''
Script to create a csv from all EnviDat records.
This rewrites some of the methods used in envidat/api/v1.py and utils.py
as this script was requested as a standalone script

Author: Ranita Pal, Swiss Federal Research Institute WSL
Date created: November 13, 2023
Date last updated: November 24, 2023
Version: 1

Instructions for usage:
    python .\scripts\metadata_to_csv.py -f <filename>
    python .\scripts\metadata_to_csv.py --file <filename>
    python <path_to_fle>\metadata_to_csv.py

Requirements:
    Python version >= 3.11

'''


# Imports
import os
import argparse
# Setup logging
import logging
import json
import csv
import requests


# Setup program logging to console (terminal)
# Check terminal for logged information, warning and error messages
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger(__name__)

def get_url(url: str) -> requests.Response:
    """Get a URL with additional error handling.

    Args:
        url (str): The URL to GET.
    """
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
        log.error(f"Unhandled exception occurred on get: {r.request.url}")

    return None

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

def format_author(author_list: str) -> str | None:
    """Formatting author name(s) in the format 
        firstname1;lastname1::firstname2;lastname2.

    Args:
        author_list (json): Multiple author names in json format.

    Returns:
        str: String of concatenated names in the format 
             firstname1;lastname1::firstname2;lastname2.
    """
    author_json = json.loads(author_list)
    all_names = ""
    for per in author_json:
        if all_names != "":
            all_names = f"{all_names}::"
        all_names = f"{all_names}{per['given_name']};{per['name']}"
    return all_names

def format_resources(resource_list: list) -> str | None:
    """Formatting resources(s) to have only required details like name, 
       restriction level and URL.

    Args:
        resource_list (list): Multiple resource dictionaries in list format.

    Returns:
        str: String of concatenated resources, each in the format 
              name;level;url::.
    """
    all_res = ""
    for res in resource_list:
        try:
            if res['restricted'] != "":
                res['restricted'] = json.loads(res['restricted'])
                res['restricted'] = res['restricted']['level']
            else:
                res['restricted'] = ""
            if all_res != "":
                all_res = f"{all_res}::"
            all_res = f"{all_res}{res['name']};{res['restricted']};{res['url']}"
        except KeyError as e:
            log.error(f"Details not found for package with name {res['name']}: {e}")
            return None
    return all_res

def format_tags(tag_dict: dict, tags: list) -> None:
    """Formatting tags to have only required details like name, 
       restriction level and URL.

    Args:
        tag_dict (dictionary): The entire dictionary for that package, 
                                since tags will be stored here.
        tags (list): The list of tags present for that package.

    Returns:
        None: Formatting already made in dictionary, nothing to return.
    """
    # keeping the maximum number of tags to 15
    tag_len = len(tags)
    for i in range(15):
        tag_dict[f"tag_{i+1}"] = tags[i]['name'] if i < tag_len else 'null'
    return

def convert_json_to_csv(filename: str) -> None:
    """Fetching all packages and formatting them to write to a csv file.

    Args:
        filename (str): The name of the csv file where all details need 
                         to be stored.
        
    Returns:
        None: CSV already written in given location, nothing to return.
    """


    try:
        resources = get_metadata_list_with_resources()
    except Exception as e:
        log.error(f"Cannot fetch metadata, error: {e}")
        return None

    csv_list = []
    # modifying info
    # put a check if resources are not empty
    for item in resources:
        csv_dict = {}
        try:
            csv_dict['title'] = item['title']
            csv_dict['name'] = item['name']
            csv_dict['author'] = format_author(item['author'])
            csv_dict['id'] = item['id']
            csv_dict['license_title'] = item['license_title']
            csv_dict['metadata_created'] = item['metadata_created']
            csv_dict['metadata_modified'] = item['metadata_modified']
            csv_dict['notes'] = item['notes']
            csv_dict['num_resources'] = item['num_resources']
            csv_dict['num_tags'] = item['num_tags']
            csv_dict['publication_state'] = item['publication_state']
            csv_dict['organization'] = item['organization']['title']
            csv_dict['resources'] = format_resources(item['resources'])
            csv_dict['resource_type'] = item['resource_type']
            csv_dict['resource_type_general'] = item['resource_type_general']
            publication = json.loads(item['publication'])
            csv_dict['publication_year'] = publication['publication_year']
            csv_dict['publisher'] = publication['publisher']
            format_tags(csv_dict, item['tags'])
        except KeyError as e:
            log.error(f"Details not found for package with "
                      f"name '{item['name']}': {e}")
            return None
        except Exception as e:
            log.error(f"Error in formatting various fields of package with name"
                      f"{item['name']}: {e}")
            return None
        csv_list.append(csv_dict)

    #write to csv file
    if len(csv_list) != 0:
        log.info(f"Finished formatting the packages. "
                 f"Starting to create CSV file: '{filename}'")
        with open(filename, 'w', newline='', encoding='utf8') as f:
            w = csv.DictWriter(f, csv_list[0].keys())
            w.writeheader()
            w.writerows(csv_list)
        log.info(f"CSV file created: '{filename}'")
    return


if __name__ == '__main__':
    # Setup argument parser
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-f', "--file",
        type=str,
        required=False,
        default='package_list.csv',
        help="Name of CSV file. Default is 'package_list.csv'",
    )
    args = parser.parse_args()

    # fetch the packages, format them and write to csv
    convert_json_to_csv(args.file)

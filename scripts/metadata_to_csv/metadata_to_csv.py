"""
Script to create a csv from all EnviDat records.

This rewrites some methods used in envidat/api/v1.py and utils.py
as this script was requested as a stand-alone script

Authors: Ranita Pal and Rebecca Kurup Buchholz, Swiss Federal Research Institute WSL
Date created: November 13, 2023
Date last updated: February 7, 2024
Version: 2

Instructions for usage:
    python .\scripts\metadata_to_csv.py -f <filename>
    python .\scripts\metadata_to_csv.py --file <filename>
    python <path_to_fle>\metadata_to_csv.py

Requirements:
    Python version >= 3.11

"""

# TODO check about "organization-hidden"


# Imports
import os
import argparse
import json
import csv
from pprint import pprint

import requests
import urllib.parse
import logging

# Setup program logging to console (terminal)
# Check terminal for logged information, warning and error messages
# Change logging level to debug to see log debug statements in terminal: logging.DEBUG
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger(__name__)


def get_url(url: str) -> requests.Response | None:
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


def get_ckan_dict(
        path: str,
        data_dict: dict[str, str] | None = None,
        host: str = "https://www.envidat.ch"
) -> dict | None:
    """Return dictionary parsed from CKAN API call response.

    Args:
        path (str): API host path, should start with "/".
                Example:  "/api/3/action/current_package_list_with_resources"
        data_dict (dict): Optional dictionary of strings with optional query parameters
            referred to as a data_dict in CKAN documentation.
            Defaults to None. Example: {"limit": "1000"}
        host (str): API host url. Attempts to get from environment if omitted.
            Defaults to call EnviDat host at "https://www.envidat.ch"

    Returns:
        dict: Dictionary parsed from JSON returned by CKAN API call.
    """

    # Get API host from environment if it exists
    if "API_HOST" in os.environ:
        log.debug("Getting API host from environment variables.")
        api_host = os.getenv("API_HOST")
    else:
        api_host = host

    # Assign URL used to call API
    api_url = f"{api_host}{path}"

    # Add query parameter(s) if they exist
    if data_dict:
        query_params = urllib.parse.urlencode(data_dict)
        api_url = f"{api_url}?{query_params}"

    log.debug(f"Calling API with URL: {api_url}")
    try:
        ckan_json = get_url(api_url).json()
    except Exception as e:
        log.exception(e)
        raise Exception(f"Failed to retrieve JSON string from call to : {api_url}")

    return ckan_json


def get_metadata_list_with_resources(sort_result: bool = None) -> list:
    """Return all current package/metadata as list of results with associated resources.

    Args:
        sort_result (bool): Sort result alphabetically by metadata name.
            Default to None.

    Note: Limits results to 100000.

    Returns:
        list: List of packages, with nested resources.
    """
    # Get package/metadata as with associated resources from API
    package_names_with_resources = get_ckan_dict(
        "/api/3/action/current_package_list_with_resources",
        {"limit": "100000"}
    )

    # Extract results and assign them to a list
    log.debug("Extracting [result] key from metadata packages.")
    package_names_with_resources = list(package_names_with_resources["result"])
    log.info(f"Returned {len(package_names_with_resources)} metadata entries from API.")

    # If sort_result true sort by name key alphabetically
    if sort_result:
        log.debug("Sorting return by nested 'name' key alphabetically.")
        package_names_with_resources = sorted(
            package_names_with_resources, key=lambda x: x["name"], reverse=False
        )

    return package_names_with_resources


def get_organization_list() -> list:
    """Return all current organizations in CKAN API as a list.

    Note: Limits results to 100000.

    Returns:
        list: List of organizations.
    """
    # Get organizations as string in JSON format
    organizations = get_ckan_dict(
        "/api/3/action/organization_list",
        {"limit": "100000"}
    )

    # Extract result key and assign value to a list
    log.debug("Extracting 'result' key from organizations_list")
    organizations_list = list(organizations["result"])
    log.debug(f"Returned {len(organizations_list)} organizations from CKAN API")

    return organizations_list


def get_organization_show(organization_id: str) -> dict:
    """Return the metadata for an organization as a dictionary.

    Arg:
        organization_id (str): id or name of CKAN organization (Ex: 'gis')

    Returns:
        dict: Dictionary with organization metadata.
    """
    # Get organization metadata as string in JSON format
    organization = get_ckan_dict(
        "/api/3/action/organization_show",
        {"id": organization_id}
    )

    # Extract result key and assign value to a dictionary
    log.debug("Extracting 'result' key from organization_show")
    organization_dict = dict(organization["result"])
    log.debug(
        f"Returned organization_show from CKAN API for organization"
        f" with id '{organization_id}'"
    )

    return organization_dict


# TODO finish logic, possibly remove function
def get_research_unit(
        organization: dict,
        wsl_name: str = "wsl",
        slf_name: str = "wsl-institute-for-snow-and-avalanche-research-slf"
) -> str:
    """Return research unit that corresponds to an organization in EnviDat CKAn API.
    For organization hiearchy see https://envidat.ch/organization

    If research unit can be found then returns string "null".

    Args:
        organization (dict): Dictionary with organization metadata.
        wsl_name (str): String with default name of WSL organization in EnviDat API.
        slf_name (str): String with default name of SLF organization in EnviDat API.

    Returns:
        str: String with name of research unit
    """
    # Assign default string of "null" for research_unit
    research_unit = "null"

    # Extract groups from organization metadata
    groups = organization.get("groups", [])

    # Assign research_unit to value that best corresponds to EnviDat
    #   organization structure
    if len(groups) > 0:

        research_unit = groups[0].get("name", "null")

        # If parent organization is WSL or SLF then assign research_unit to
        #  organization's name
        if research_unit in [wsl_name, slf_name]:
            research_unit = organization.get("name")

    return research_unit


# TODO finish and document test function
def get_organizations_titles_parent(
        slf_name: str = "wsl-institute-for-snow-and-avalanche-research-slf"
) -> tuple[dict, dict]:
    orgs_titles = {}
    child_parent = {}

    # Get list of organizations
    organizations = get_organization_list()

    # Remove Trusted Users Organization from list
    if "trusted" in organizations:
        organizations.remove("trusted")

    for org in organizations:

        # Get metadata for an organization
        org_show = get_organization_show(org)

        # Extract organization title and assign to orgs_title dictionary
        orgs_titles[org] = org_show.get("title", "null")

        # Extract groups from organization metadata
        groups = org_show.get("groups", [])

        # Assign research_unit to value that best corresponds to EnviDat
        #   organization structure
        if org == slf_name:
            research_unit = org
        elif len(groups) > 0:
            research_unit = groups[0].get("name", org)
        else:
            research_unit = org

        child_parent[org] = research_unit

    return orgs_titles, child_parent


# TODO finish WIP and test and document function
def is_root_envidat_org(org_name: str, child_parent: dict) -> bool:
    if child_parent.get(org_name) == org_name:
        return True
    return False


# TODO finish WIP and test refactored function
# TODO replace names with titles from orgs_titles
# TODO review test output with https://envidat.ch/organization
def get_organizations_hierarchy() -> dict[str, str]:
    """Return dictionary of CKAN API organizations hierarchy that uses algorithm
        to assign research unit in format {"child_org_name": "parent_org_title"}

    Includes all organizations in CKAN database.

    Example output:
        {
            'dynamic-macroecology': 'Land Change Science',
            'ecological-genetics': 'Biodiversity and Conservation Biology'
        }
    """
    # Assign dictionary to contain processed organizations hierarchy
    orgs_hierarchy = {}

    # Get organization titles and child_parent dictionaries
    orgs_titles, child_parent_dict = get_organizations_titles_parent()

    for child, parent in child_parent_dict.items():

        if is_root_envidat_org(child, child_parent_dict):
            orgs_hierarchy[child] = "ROOT"
        elif is_root_envidat_org(parent, child_parent_dict):
            orgs_hierarchy[child] = "RESEARCH UNIT"
        else:
            orgs_hierarchy[child] = "GROUP"

    return orgs_hierarchy


# TODO remove old function
# def get_organizations_hierarchy() -> dict[str, str]:
#     """Return dictionary of CKAN API organizations hierarchy that uses algorithm
#         to assign research unit in format {"child_org_name": "parent_org_title"}
#
#     Includes all organizations in CKAN database.
#
#     Example output:
#         {
#             'dynamic-macroecology': 'Land Change Science',
#             'ecological-genetics': 'Biodiversity and Conservation Biology'
#         }
#     """
#
#     orgs_hierarchy = {}
#     orgs_titles = {}
#
#     organizations = get_organization_list()
#
#     for org in organizations:
#
#         # Get metadata for an organization
#         org_show = get_organization_show(org)
#
#         # Extract organization title and assign to orgs_title dictionary
#         orgs_titles[org] = org_show.get("title", "null")
#
#         # Old block
#         # groups = org_show.get("groups", [])
#         # if len(groups) > 0:
#         #     research_unit = groups[0].get("name", "null")
#         # else:
#         #     research_unit = "null"
#
#         # Test block
#         # Get research unit that corresponds to organization and
#         # assign to orgs_hierarchy dictionary
#         research_unit = get_research_unit(org_show)
#         orgs_hierarchy[org] = research_unit
#
#     # Replace parent_org names with titles
#     for child_org, parent_org in orgs_hierarchy.items():
#         if parent_org in orgs_titles.keys():
#             orgs_hierarchy[child_org] = orgs_titles[parent_org]
#
#     return orgs_hierarchy


def format_author(author_list: str) -> str | None:
    """Formatting author name(s) in the format 
        firstname1;lastname1::firstname2;lastname2

        First names (referred to as 'given_name') are truncated to first letter
        with a period. Example:   Andrea  ->  A.

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

        if len(per.get("given_name", "")) > 0:
            given_name = f"{((per['given_name'])[0]).upper()}."
        else:
            given_name = per["given_name"]

        all_names = f"{all_names}{given_name};{per['name']}"

    return all_names


def format_affiliation(author_list: str) -> str:
    """Formatting author affiliation(s) in the format
        <author1_affiliation>::<author2_affiliation>

        Example:
            WSL::EPFL::University of Zurich

    If affiliation not found then affiliation is
    assigned as string: 'null'

    Args:
        author_list (json): Multiple author names in json format.

    Returns:
        str: String of concatenated affiliations in the format
              <author1_affiliation>::null::<author3_affiliation>
    """
    author_json = json.loads(author_list)
    all_affiliations = ""

    for author in author_json:

        if all_affiliations != "":
            all_affiliations = f"{all_affiliations}::"

        all_affiliations = f"{all_affiliations}{author.get('affiliation', 'null')}"

    return all_affiliations


def format_data_credit(author_list: str) -> str:
    """Formatting author data credits(s) in the format shown in the following example:
        software;curation::null::supervision::software;supervision

    If data credit(s) not found then assigned as string: 'null'

    Args:
        author_list (json): Multiple author names in json format.

    Returns:
        str: String of concatenated data credits in the format
              software;curation::null::supervision
    """
    author_json = json.loads(author_list)
    all_data_credits = ""

    for author in author_json:

        if all_data_credits != "":
            all_data_credits = f"{all_data_credits}::"

        data_credit = author.get("data_credit", ["null"])

        if isinstance(data_credit, list):
            data_credit = ';'.join(data_credit)

        all_data_credits = f"{all_data_credits}{data_credit}"

    return all_data_credits


def format_date(date: str) -> str:
    """Formatting date(s) in the format:
        date1;date_type1::date2;date_type2

    If value not found then assignes as string: 'null'

    Args:
        date (json): date list in json string format

    Returns:
        str: String of concatenated dates in the format
             date1;date_type1::date2;date_type2
    """
    dates = json.loads(date)
    all_dates = ""

    for dte in dates:

        if all_dates != "":
            all_dates = f"{all_dates}::"

        all_dates = f"{all_dates}{dte.get('date', 'null')};{dte.get('date_type', 'null')}"

    return all_dates


def format_funding(funding: str) -> str:
    """Formatting funding institutions in the format shown in the following example:
        WSL::EPFL::WSL

     If funding instituion not found then assigned as string: 'null'

    Args:
        funding (json): funding list in json string format

    Returns:
        str: String of concatenated funding instituions in the formst
                WSL::EPFL::WSL
    """
    funders = json.loads(funding)
    all_funders = ""

    for funder in funders:

        if all_funders != "":
            all_funders = f"{all_funders}::"

        all_funders = f"{all_funders}{(funder.get('institution', 'null')).strip()}"

    return all_funders


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
        tag_dict[f"tag_{i + 1}"] = tags[i]['name'] if i < tag_len else 'null'
    return


def convert_json_to_csv(filename: str) -> None:
    """Fetching all packages and formatting them to write to a csv file.

    Args:
        filename (str): The name of the csv file where all details need 
                         to be stored.
        
    Returns:
        None: CSV already written in given location, nothing to return.
    """

    # Get package metadata from CKAN API
    try:
        resources = get_metadata_list_with_resources()
    except Exception as e:
        log.error(f"Cannot fetch metadata, error: {e}")
        return None

    # Get organizations hierarchy dictionary (in format {"child_org": "parent_org"}
    try:
        orgs_hierarchy = get_organizations_hierarchy()
        pprint(orgs_hierarchy)  # TODO remove
    except Exception as e:
        log.error(f"Cannot get organization hierarchy, error: {e}")
        return None

    csv_list = []
    # modifying info
    # put a check if resources are not empty
    for item in resources:

        csv_dict = {}

        try:
            csv_dict['title'] = item['title']
            csv_dict['name'] = item['name']
            csv_dict['id'] = item['id']
            csv_dict['author'] = format_author(item['author'])
            csv_dict['affiliation'] = format_affiliation(item['author'])
            csv_dict['data_credit'] = format_data_credit(item['author'])
            csv_dict['date'] = format_date(item['date'])
            csv_dict['funding'] = format_funding(item['funding'])
            csv_dict['license_title'] = item['license_title']
            csv_dict['license_url'] = item[
                'license_url'] if 'license_url' in item else ''
            csv_dict['metadata_created'] = item['metadata_created']
            csv_dict['metadata_modified'] = item['metadata_modified']
            csv_dict['notes'] = item['notes']
            csv_dict['num_resources'] = item['num_resources']
            csv_dict['num_tags'] = item['num_tags']
            csv_dict['publication_state'] = item['publication_state']
            csv_dict['organization'] = item['organization']['title']
            csv_dict['research_unit'] = orgs_hierarchy[item['organization']['name']]
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

    # write to csv file
    if len(csv_list) != 0:
        log.info(f"Finished formatting the packages. "
                 f"Starting to create CSV file: '{filename}'")

        # Encoding is 'utf-8-sig' so that Microsoft Excel can detect UTF-8 encoding of s
        # pecial characters including umlauts
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
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

    # TODO revert commented out function
    # fetch the packages, format them and write to csv
    # convert_json_to_csv(args.file)

    # TODO remove tests
    # TESTS

    orgs_titles1, child_parent1 = get_organizations_titles_parent()
    # pprint(orgs_titles1)
    # pprint('\n\n\n')
    pprint(child_parent1)
    pprint('\n\n\n')

    orgs_hierarchy_test = get_organizations_hierarchy()
    pprint(orgs_hierarchy_test)

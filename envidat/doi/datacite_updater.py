import logging

# Setup logging
from logging import getLogger

import requests

from envidat.api.v1 import get_envidat_record
from envidat.doi.datacite_publisher import publish_datacite
from envidat.utils import get_response_json

log = getLogger(__name__)
log.setLevel(level=logging.INFO)

# Setup up file log handler
logFileFormatter = logging.Formatter(
    fmt="%(levelname)s %(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
# TODO implement name of log file as command line argument, assign default name
fileHandler = logging.FileHandler(filename="./logs/datacite_updater.log")
fileHandler.setFormatter(logFileFormatter)
fileHandler.setLevel(level=logging.INFO)
log.addHandler(fileHandler)

# Load config from environment variables
load_dotenv_if_in_debug_mode(".env")


def datacite_update_all_records():
    """Updates existing DOIs for all EnviDat records on DataCite.

    Function converts all EnviDat records to DataCite Metadata Schema 4.4,
    for documentation: https://schema.datacite.org/meta/kernel-4.4/

    For documentation of DataCite API: https://support.datacite.org/docs/api

    For DataCite API reference:
    https://support.datacite.org/reference/introduction

    For documentation of DataCite API endpoint that updates DOIs:
    https://support.datacite.org/reference/put_dois-id
    """
    # Get EnviDat DOIs on DataCite
    dc_dois = get_dc_dois()

    # Handle if dc_dois are None
    if not dc_dois:
        log.error("Failed to get DataCite DOIs")
        return None

    # Get EnviDat record objects for record that are published and have DOIs
    published_records = get_published_record_names_with_dois()

    # Handle if published_records are None
    if not published_records:
        log.error("Failed to get EnviDat published records names that have DOIs")

    # Update or create new DOIs in DataCite for all EnviDat records
    for record in published_records:

        dc_response = datacite_update_one_record(record.get("name"))

        # Log successful update
        # Unsuccessful update error messages logged
        # during call to datacite_update_one_record()
        if dc_response:
            log.info(dc_response)
            continue

    return


def datacite_update_records(record_names: list[str]):
    """Updates existing DOIs for EnviDat records on DataCite.

    ASSUMPTION: Records already exist on DataCite and should be updated.

    Function converts EnviDat records to DataCite Metadata Schema 4.4, for
    documentation: https://schema.datacite.org/meta/kernel-4.4/

    For documentation of DataCite API: https://support.datacite.org/docs/api

    For DataCite API reference:
    https://support.datacite.org/reference/introduction

    For documentation of DataCite API endpoint that updates DOIs:
    https://support.datacite.org/reference/put_dois-id

    Args:
        record_names (list[str]): List of EnviDat records names that should be
            updated. Example: ["mountland-jura", "envidat-lwf-51"]
    """
    # Update DOIs in DataCite for EnviDat record_names
    for name in record_names:

        dc_response = datacite_update_one_record(name)

        # Log successful update
        # Unsuccessful update error messages logged
        # during call to datacite_update_one_record()
        if dc_response:
            log.info(dc_response)
            continue

    return


def datacite_update_one_record(name: str, dc_dois: list[str] = None) -> dict | None:
    """Updates existing DOI for one EnviDat record on DataCite.

    ASSUMPTION: Record already exists on DataCite and should be updated.

    Function converts EnviDat record to DataCite Metadata Schema 4.4, for
    documentation: https://schema.datacite.org/meta/kernel-4.4/

    For documentation of DataCite API: https://support.datacite.org/docs/api

    For DataCite API reference:
    https://support.datacite.org/reference/introduction

    For documentation of DataCite API endpoint that updates DOIs:
    https://support.datacite.org/reference/put_dois-id

    Args:
        name (str): EnviDat records name that should be updated.
            Example: "mountland-jura"
        dc_dois (list[str]) :  List of DOIs with a specified DOI prefix in
          DataCite. This prefix is assigned in the config to the EnviDat
          prefix in DataCite.
          This arg is used during update of
          all records in datacite_update_all_records()
          Default value is None.

    Returns:
        dict/None: Returns dictionary with DataCite response data.
            If update fails then returns None.
    """
    try:
        # Get EnviDat record from CKAN API
        envidat_record = get_envidat_record(name)

        # Extract result from record
        result = envidat_record.get("result")

        # Check that result is truthy
        if not result:
            log.error(
                f"Failed to get 'result' from EnviDat record with " f"name '{name}'"
            )
            return

        # Check status code of response from call to CKAN API
        status_code = envidat_record.get("status_code")
        if status_code != 200:
            log.error(
                f"Failed to get EnviDat record with "
                f"name:  '{name}', "
                f"status_code:  {status_code}, "
                f"error:  {result}"
            )
            return

        # If dc_dois is truthy then check if doi not in dc_dois
        if dc_dois:
            doi = result.get("doi")
            if doi not in dc_dois:
                log.error(
                    f"EnviDat record with name '{name}' "
                    f"and doi '{doi} not in DataCite DOIs"
                )
                return

        # Update record with existing DOI in DataCite
        dc_response = publish_datacite(result, is_update=True)

        # Check that dc_response is dictionary
        if type(dc_response) != dict:
            log.error(
                f"Failed to update EnviDat record with name '"
                f"{name}', check console logs"
            )
            return

        # Add record name to dc_response
        dc_response["name"] = name

        # Return response for updated record, expecting a status code of 200
        if dc_response.get("status_code") == 200:
            return dc_response
        # Else log response for unexpected DataCite response status codes
        else:
            log.error(
                f"Failed to update record in DataCite with "
                f"name '{name}', error:  {dc_response}"
            )
            return

    except AttributeError as e:
        log.error(
            f"Failed to update record in DataCite with name '{name}', " f"error: {e}"
        )
        return


def get_dc_dois(num_records: int = 10000) -> list[str] | None:
    """Return a list of DOIs with a specified DOI prefix in DataCite.

    "DOI_PREFIX" in config is set to prefix assigned to EnviDat in DataCite.

    For DataCite API documentation of endpoint to get list of DOIs see:
    https://support.datacite.org/docs/api-get-lists

    Args:
        num_records (int): Number of records to retrieve from DORA API.
        Default value is 10000.
    """
    # Extract variables from config needed to call DataCite API
    # NOTE: List of DOIs should not be obtained from DataCite "test" API
    try:
        api_url = os.environ("DOI_API_URL")
        prefix = os.environ("DOI_PREFIX")
    except KeyError as e:
        log.error(f"KeyError: {e} does not exist in config")
        return None

    # Add prefix query param to url
    # Add page[size] param retrieve up to 10000 (default) records on the page
    api_url = f"{api_url}?prefix={prefix}&page[size]={num_records}"

    # Call API
    r = requests.get(api_url)

    # Return DOIs is successful
    if r.status_code == 200:

        # Get DOIs stored in record "id" values
        data = r.json().get("data")
        dois = [record.get("id") for record in data]

        # Return DOIs
        if dois:
            return dois
        else:
            log.error("Failed to get DOIs")
            return None

    # Else log error message and return none
    else:
        log.error("Failed to get DOIs")
        return None


# TODO implement error handling (try/excpet)
def get_published_record_names_with_dois() -> list[dict] | None:
    """Return EnviDat record names that have a DOI and a "publication_state"
    value of "published".

    Logs records that do not have a DOI or have a DOI but a
    "publication_state" value of "reserved".

    Returns: list[dict]/None: List of record name dictionaries with "name"
              and "doi" keys. Returns None if failed to obtain list.
    """
    err_message = "Failed to get names of published records with DOIs."

    # Get JSON response from call to CKAN
    # "API_CURRENT_PACKAGE_LIST_WITH_RESOURCES" endpoint
    response_json = get_response_json(
        api_host="API_HOST",
        api_path="API_CURRENT_PACKAGE_LIST_WITH_RESOURCES",
        query={"limit": 100000},
    )

    # Extract and return record names from records that have a DOI and are
    # published
    if response_json:

        records = response_json["result"]
        if records:
            published_records = []

            for record in records:
                # TODO review condition
                if record.get("doi") and record.get("publication_state") == "published":
                    published_records.append(
                        {"name": record.get("name"), "doi": record.get("doi")}
                    )

                # Log records that have a value for the "doi" key
                # and a "reserved" value for the "publication_state" value
                # but are not in dc_dois
                elif (
                    record.get("doi") and record.get("publication_state") == "reserved"
                ):
                    log.warning(
                        f"Record '{record.get('name')}' "
                        f"with DOI {record['doi']} "
                        f" has a 'publication_state' value of"
                        f" '{record['publication_state']}' and is not "
                        f"published on "
                        f"DataCite"
                    )

                # Log warning for records that have a "doi" value of empty
                # string ""
                elif record.get("doi") == "":
                    log.warning(f"Record does not have a DOI:'{record.get('name')}'")

            return published_records

        else:
            log.error(err_message)
            return None

    else:
        log.error(err_message)
        return None

import logging

import requests
from dotenv import dotenv_values

from envidat.api.v1 import get_envidat_record
from envidat.doi.datacite_publisher import publish_datacite
from envidat.utils import get_response_json

# Setup logging
from logging import getLogger
log = getLogger(__name__)
log.setLevel(level=logging.INFO)

# Setup up file log handler
logFileFormatter = logging.Formatter(
    fmt=f"%(levelname)s %(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")
fileHandler = logging.FileHandler(filename='datacite_importer.log')
fileHandler.setFormatter(logFileFormatter)
fileHandler.setLevel(level=logging.INFO)
log.addHandler(fileHandler)


# TODO write documentation for this importer

# TODO write logic to handle None values returned from helpers
# TODO implement try/except error handling
# TODO write docstring
def datacite_create_and_update_all_records():
    """Creates new DOIs and updates existing DOIs for EnviDat records on DataCite.

       Function converts all EnviDat records to DataCite Metadata Schema 4.4, for
       documentation see https://schema.datacite.org/meta/kernel-4.4/
    """

    # Get EnviDat DOIs on DataCite
    dc_dois = get_dc_dois()

    # Get EnviDat record objects for record that are published and have DOIs
    published_records = get_published_record_names_with_dois()

    # TODO remove counter code after testing
    # counter = 0
    # Update or create new DOIs in DataCite for all EnviDat records
    for record in published_records:

        # Get EnviDat record from CKAN API
        envidat_record = get_envidat_record(record.get("name"))

        # Extract package from record result
        package = envidat_record.get("result")

        # Update existing DOIs already existing in DataCite
        if record["doi"] in dc_dois:
            dc_response = publish_datacite(package, is_update=True)
        # Else create new DOIs in DataCite
        else:
            dc_response = publish_datacite(package, is_update=False)

        # Add package name to dc_reponse
        dc_response["name"] = record.get("name")

        # Log response for updated and created records
        if dc_response["status_code"] in [200, 201]:
            log.info(dc_response)
        # Else log response for unexpected DataCite response status codes
        else:
            log.error(dc_response)

        # counter += 1
        # if counter > 25:
        #     break

    return


# TODO write docstring
def get_dc_dois(num_records: int = 10000) -> list[str] | None:
    """Return a list of DOIs in DataCite.

       "DOI_PREFIX" in config is set to prefix assigned to EnviDat in DataCite.

       For DataCite API documentation of endpoint to get list of DOIs see:
       https://support.datacite.org/docs/api-get-lists
    """

    # Load config from environment vairables
    config = dotenv_values(".env")

    # Extract variables from config needed to call DataCite API
    try:
        api_url = config["DATACITE_API_URL"]
        prefix = config["DOI_PREFIX"]
    except KeyError as e:
        log.error(f'KeyError: {e} does not exist in config')
        return None

    # Add prefix query param to url
    # Add page[size] param retrieve up to 10000 (default) records on the page
    api_url = f"{api_url}?prefix={prefix}&page[size]={num_records}"

    # Call api
    r = requests.get(api_url)

    # Return DOIs is successful
    if r.status_code == 200:

        # Get DOIs stored in record "id" values
        data = r.json().get('data')
        dois = [record.get("id") for record in data]

        # Return DOIs
        if dois:
            return dois
        else:
            log.error(f"Failed to get DOIs")
            return None

    # Else log error message and return none
    else:
        log.error(f"Failed to get DOIs")
        return None


# TODO implement error handling (try/excpet)
# TODO write docstring
def get_published_record_names_with_dois() -> list[dict] | None:
    """
    """

    err_message = "Failed to get names of published records with DOIs."

    # Get JSON response from call to CKAN
    # "API_CURRENT_PACKAGE_LIST_WITH_RESOURCES" endpoint
    response_json = get_response_json(api_host="API_HOST",
                                      api_path=
                                      "API_CURRENT_PACKAGE_LIST_WITH_RESOURCES",
                                      query={"limit": 100000})

    # Extract and return record names from records that have a DOI and are published
    if response_json:

        records = response_json["result"]
        if records:
            published_records = []

            for record in records:
                # TODO review condition
                if record.get("doi") and record.get("publication_state") == "published":
                    published_records.append({
                        "name": record.get("name"),
                        "doi": record.get("doi")
                    })

            return published_records

        else:
            log.error(err_message)
            return None

    else:
        log.error(err_message)
        return None

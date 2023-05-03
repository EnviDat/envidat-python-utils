import base64
import json
from logging import getLogger

import requests
from dotenv import dotenv_values

from envidat.converters.datacite_converter import convert_datacite

log = getLogger(__name__)


# TODO review if DOIs should continue to be reserved in CKAN database!!!!

# TODO note in documentation for config that environment variables with a hash
#   must be enclosed in quotes

# TODO review where to store environment variables

# TODO review dependencies management with PDM


def reserve_draft_doi_datacite(metadata_record: dict) -> str | None:
    """Reserve a DOI identifer in "Draft" state with DataCite.

       If DOI not available from input metadata_record then new DOI
       generated by DataCite (using default EnviDat DOI suffix in config.)

       For DataCite documentation of this process see:
       https://support.datacite.org/docs/api-create-dois#create-an-identifier-in-draft-state

    Args:
        metadata_record (dict): Individual EnviDat metadata entry record dictionary.

    Returns:
        str|None: DOI reserved in DataCite or None if DOI reservation failed
    """
    # Load config from environment vairables
    config = dotenv_values(".env")

    # Extract variables from config needed to call DataCite API
    try:
        api_url = config["DATACITE_API_URL"]
        client_id = config["DATACITE_CLIENT_ID"]
        password = config["DATACITE_PASSWORD"]
        doi_prefix = config["DOI_PREFIX"]
    except KeyError as e:
        log.error(f"KeyError: {e} does not exist in config")
        return None

    payload = {"data": {"type": "dois"}}

    # If DOI already exists then include it in payload
    doi = metadata_record.get("doi")
    if doi:
        payload["data"]["attributes"] = {"doi": doi}
    # Else instruct DataCite API to auto-generate DOI by only adding
    # "prefix" attribute to payload, this auto-generates a random DOI suffix
    else:
        payload["data"]["attributes"] = {"prefix": doi_prefix}

    # Convert payload to JSON and then send POST request to DataCite API
    payload_json = json.dumps(payload)
    headers = {"Content-Type": "application/vnd.api+json"}

    r = requests.post(
        api_url, headers=headers, auth=(client_id, password), data=payload_json
    )

    # Return DOI
    if r.status_code == 201 or r.status_code == 200:
        reserved_doi = r.json().get("data").get("id")
        if reserved_doi:
            return reserved_doi
        else:
            log.error(
                f"Error cannot parse reserved DOI from DataCite response: "
                f"{r.json()}"
            )
            return None
    else:
        log.error(f"Error reserving DOI on DataCite:  " f"HTTP Code {r.status_code}")
        log.error(f"Error:{r.json()}")
        return None


# TODO investigate not reserving DOI at DataCite and instead directly
#  publish new dataset by reserving DOI within CKAN or other database
def publish_datacite(metadata_record: dict, is_update=False) -> dict | None:
    """Publish a EnviDat record in EnviDat using the "publish" event.

       Converts EnviDat record to DataCite XML format before publication.

       For DataCite documentation of this process see:
       https://support.datacite.org/docs/api-create-dois#changing-the-doi-state
       https://support.datacite.org/docs/api-create-dois#provide-metadata-in-formats
       -other-than-json

    Args:
        metadata_record (dict): Individual EnviDat metadata entry record
                                    dictionary.
        is_update (bool): If true then updates existing DOI,
                          else creates new DOI.
                          Default value is False.

    Returns:
        str/None: DOI reserved in DataCite or None if DOI reservation failed
    """
    # Load config from environment vairables
    config = dotenv_values(".env")

    # Extract variables from config needed to call DataCite API
    try:
        api_url = config["DATACITE_API_URL"]
        client_id = config["DATACITE_CLIENT_ID"]
        password = config["DATACITE_PASSWORD"]
        site_url = config["SITE_DATASET_URL"]
    except KeyError as e:
        log.error(f"KeyError: {e} does not exist in config")
        return None

    # Get DOI
    doi = metadata_record.get("doi")
    if not doi:
        log.error("ERROR record does not have a 'doi' value")
        return None

    # Get metadata record URL
    name = metadata_record.get("name", metadata_record["id"])
    url = f"{site_url}/{name}"

    # Convert metadata record to DataCite XML and encode to base64 formatted
    # string
    xml = convert_datacite(metadata_record)
    if xml:
        xml_encoded = xml_to_base64(xml)
    else:
        log.error("ERROR unable to convert record to DataCite XML format")
        return None

    # Create payload
    payload = {
        "data": {
            "id": doi,
            "type": "dois",
            "attributes": {
                "event": "publish",
                "doi": doi,
                "url": url,
                "xml": xml_encoded,
            },
        }
    }

    # Convert payload to JSON
    payload_json = json.dumps(payload)
    headers = {"Content-Type": "application/vnd.api+json"}

    # If is_update is True update DOI that is already registered
    if is_update:
        api_url = f"{api_url}/{doi}"
        r = requests.put(
            api_url, headers=headers, auth=(client_id, password), data=payload_json
        )
    # Else create new DOI
    else:
        r = requests.post(
            api_url, headers=headers, auth=(client_id, password), data=payload_json
        )

    # Return DOI if successful, else return error message
    # Status code 201 indicates a new DOI was created
    # Status code 200 indicates an existing DOI was updated
    # TODO implement try/except error handling
    # TODO use get() method on status_code
    if r.status_code == 201 or r.status_code == 200:
        published_doi = r.json().get("data").get("id")
        if published_doi:
            return {"status_code": r.status_code, "result": published_doi}
        else:
            return {
                "status_code": 500,
                "result": f"Failed to parse published DOI from DataCite "
                f"response: {r.json()}",
            }
    else:
        return {
            "status_code": r.status_code,
            "result": f"Failed publishing DOI {doi} on DataCite:  {r.json()}",
        }


def xml_to_base64(xml: str) -> str:
    """Converts XML formatted string to base64 formatted string.

       Returns string in base64 format (not bytes)

    Args:
        xml (str): String in XML format

    Returns:
        str: base64 formatted string conversion of input xml_str
    """
    if isinstance(xml, str):
        xml_bytes = xml.encode("utf-8")
        xml_encoded = base64.b64encode(xml_bytes)
        xml_str = xml_encoded.decode()
        return xml_str

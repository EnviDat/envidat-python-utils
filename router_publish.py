from envidat.api.v1 import get_envidat_record
from envidat.doi.datacite_publisher import publish_datacite
from fastapi import APIRouter, Response
import logging

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/publish",
    tags=["publish"]
)


# TODO implement authentication, likely with JWT tokens
# TODO check if AttributeError is best way to handle unknown errors
# TODO investigate how to add schema to API documentation on /docs
# TODO test triggering all errors
@router.get("", tags=["publish"])
def publish(name: str, response: Response):

    # Get EnviDat record from CKAN API call
    try:
        record = get_envidat_record(name)

        # Handle HTTP errors from CKAN API call
        status_code = record.get("status_code")
        if status_code != 200:
            response.status_code = status_code
            return {"error": record["result"]}

    except AttributeError as e:
        log.error(e)
        response.status_code = 500
        return {"error": "Failed to extract package as JSON from CKAN API, check logs"}

    # Publish package to DataCite and return DOI
    try:
        package = record["result"]
        dc_response = publish_datacite(package)

        # Assign response status_code
        dc_status_code = dc_response.get("status_code")
        response.status_code = dc_status_code

        # Handle HTTP errors from publishing to DataCite
        if dc_status_code != 201:
            return {"error": dc_response.get("result")}

        # Else return published DOI
        return {"doi": dc_response.get("result")}

    except AttributeError as e:
        log.error(e)
        response.status_code = 500
        return {
            "error": "Failed to extract publish EnviDat record to DataCite, check logs"}

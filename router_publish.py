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
# TODO check if 500 is best default error status code
# TODO investigate how to add schema to API documentation on /docs
# TODO test triggering all errors
@router.get("/datacite", tags=["publish"])
def publish_to_datacite(name: str, response: Response):

    # Get EnviDat record from CKAN API call
    try:
        record = get_envidat_record(name)

        # Handle HTTP errors from CKAN API call (default status_code is 500)
        status_code = record.get("status_code", 500)
        if status_code != 200:
            response.status_code = status_code
            return {"error": record.get("result",
                                        "Failed to extract record as JSON from CKAN "
                                        "API, check logs")}
    except AttributeError as e:
        log.error(e)
        response.status_code = 500
        return {"error": "Failed to extract record as JSON from CKAN API, check logs"}

    # Publish package to DataCite and return DOI
    try:
        # Extract package from record result
        package = record.get("result")

        # Publish package to DataCite
        if package:
            dc_response = publish_datacite(package)
        else:
            response.status_code = 500
            return {"error": "Failed to extract 'result' from record"}

        # Assign response status_code (default status_code is 500)
        dc_status_code = dc_response.get("status_code", 500)
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

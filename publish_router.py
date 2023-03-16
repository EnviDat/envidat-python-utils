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
# TODO test with package 'id' value
# TODO investigate how to add schema to API documentation on /docs
@router.get("", tags=["publish"])
def publish(name: str, response: Response):

    # Get EnviDat record from CKAN API call
    try:
        record = get_envidat_record(name)
        # Handle errors
        status_code = record.get("status_code")
        if status_code != 200:
            response.status_code = status_code
            return {
                "status_code": status_code,
                "result": record["result"]
            }
    except AttributeError as e:
        log.error(e)
        return {
            "status_code": 500,
            "result": "Failed to extract package as JSON from API, check logs"
        }

    # Publish package to DataCite
    try:
        package = record["result"]
        dc_response = publish_datacite(package)
        dc_status_code = dc_response.get("status_code")
        response.status_code = dc_status_code
        return dc_response
    except AttributeError as e:
        log.error(e)
        return {
            "status_code": 500,
            "result": "Failed to extract publish EnviDat record to DataCite, check logs"
        }

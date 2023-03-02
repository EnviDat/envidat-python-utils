import requests
import base64
import logging

log = logging.getLogger(__name__)


# TODO finish function
# TODO call conversion function instead of directly, use a "pkg" arguguent,
#  see ckanext/datacite_publication/datacite_publisher.py
def publish_datacite(url: str,
                     auth: tuple,
                     doi: str,
                     xml_data: str,
                     headers="Content-Type: application/vnd.api+json"
                     ) -> requests.Response:
    """Publish package data to a DataCite URL with additional error handling.
    TODO handle creating new DOI

    Args:
        url (str): DataCite URL to PUT package data
        auth (tuple): Authorization tuple in format ('user', 'pass')
        doi (str): DOI assigned to newly published package
        xml_data (str): XML input data of EnviDat package
        headers (str): Defaults to "Content-Type: application/vnd.api+json"
    """
    try:
        log.debug(f"Attempting to get {url}")
        # r = requests.put(url, data=payload)
        r = requests.put(url, headers=headers, auth=auth)
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


def xml_to_base64(xml: str):
    """Converts XML formatted string to base64 format.

    Args:
        xml (str): String in XML format

    Returns:
        str: base64 string conversion of input xml_str
    """
    if isinstance(xml, str):
        xml_bytes = xml.encode('utf-8')
        xml_encoded = base64.b64encode(xml_bytes)
        return xml_encoded

"""Converter: EnviDat API Format to XML Format"""


import logging
from xmltodict import unparse
from envidat.api.v1 import get_metadata_json_with_resources

log = logging.getLogger(__name__)


def convert_xml(package: dict) -> str:
    """
    Converter function for EnviDat record to XML format.

    :return: XML file

    """

    root = {'root': package}

    # Try to convert packages (i.e. records with metadata) to XML format
    try:
        converted_data_xml = unparse(root, short_empty_elements=True, pretty=True)
        return converted_data_xml

    except Exception as e:
        log.error("ERROR: Cannot convert EnviDat packages to XML format.")
        log.error(e)


def convert_xml_all_resources() -> str:
    """
    Converter function for EnviDat JSON records to XML format. JSON --> XML.

    :return: XML file

    Note: only valid for metadata schema of EnviDat.
    """

    metadata_json = get_metadata_json_with_resources()

    # TODO verify which root element is required for XML format
    metadata_json = {'root': metadata_json}

    # Try to convert packages (i.e. records with metadata) to XML format
    try:
        converted_data_xml = unparse(metadata_json, short_empty_elements=True, pretty=True)
        return converted_data_xml

    except Exception as e:
        log.error("ERROR: Cannot convert EnviDat packages to XML format.")
        log.error(e)

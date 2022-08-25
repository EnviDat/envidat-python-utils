"""Get EnviDat metadata records in various formats."""

import json
import logging
from typing import Literal, NoReturn, Union

from envidat.api.v1 import get_metadata_list_with_resources, get_package
from envidat.converters.iso_converter import convert_iso
from envidat.converters.xml_converter import convert_xml

log = logging.getLogger(__name__)


def validate_json(json_data):
    """Test if JSON parses and is valid."""
    try:
        json.loads(json_data)
    except ValueError:
        return False
    return True


class Record:
    """Class manipulate an EnviDat record in various ways."""

    content = None

    def __init__(
        self,
        input_data: Union[str, dict],
        extract: Literal["str", "xml", "iso"] = None,
    ) -> NoReturn:
        """
        Init the Record object.

        Only one argument should be passed for data format.

        Args:
            input_data [str, dict]: Data input, in JSON or dict form.
                Can also accept a package name to extract a record from the API.
            extract ["str", "xml", "iso"]: Extract the content immediately,
                converted to specified type.
        """
        if isinstance(input_data, dict):
            log.debug("Dictionary input provided, reading as JSON")
            self.content = json.dumps(input, indent=4)

        elif isinstance(input_data, str):
            if validate_json(input_data):
                log.debug("Valid input JSON parsed")
                self.content = input_data
            else:
                log.debug("Attempting to get package JSON from API")
                self.content = get_package(input_data)

        else:
            log.error("Input is not a valid type from (str,dict)")
            raise TypeError("Input must be of type string or dict")

        if extract:
            mapping = {
                "str": self.to_string,
                "xml": self.to_xml,
                "iso": self.to_iso,
            }
            mapping[extract]()
            return self.get_content()

    def get_content(self) -> str:
        """Get current content of Record."""
        return self.content

    def validate(self) -> bool:
        """Validate JSON record."""
        return validate_json(self.input)

    def to_string(self) -> str:
        """Convert content to string."""
        return json.dumps(self.content)

    def to_xml(self) -> str:
        """Convert content to XML record."""
        return convert_xml(self.content)

    def to_iso(self) -> str:
        """Convert content to ISO record."""
        return convert_iso(self.content)


def get_all_metadata_as_record_list(as_xml: bool = False, as_iso: bool = False) -> list:
    """
    Return all EnviDat metadata entries as Record objects.

    Defaults to standard Record, content in json format.

    Args:
        as_xml (bool): convert Record content to XML format.
        as_iso (bool): convert Record content to ISO format.

    Returns:
        list: Of Record entries for EnviDat metadata.
    """
    metadata = get_metadata_list_with_resources()
    record_list = []
    for json_entry in metadata:
        if as_xml:
            record_list.append(Record(package_json=json_entry).to_xml())
        elif as_iso:
            record_list.append(Record(package_json=json_entry).to_iso())
        else:
            record_list.append(Record(package_json=json_entry))
    return record_list

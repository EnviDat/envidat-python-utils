"""Get EnviDat metadata records in various formats."""

import json
import logging
from typing import NoReturn

from envidat.api.v1 import get_metadata_list_with_resources, get_package
from envidat.converters.iso import convert_iso
from envidat.converters.xml import convert_xml

log = logging.getLogger(__name__)


class Record:
    """Class manipulate an EnviDat record in various ways."""

    def __init__(
        self,
        package_json: str = None,
        package_dict: dict = None,
        package_name: str = None,
    ) -> NoReturn:
        """
        Init the Record object.

        Only one argument should be passed for data format.

        Args:
            package_json (str): JSON input.
            package_dict (dict): dictionary input.
            package_name (str): package name input string, calls API for JSON.
        """
        # if package_json and package_dict and package_name:
        #     raise TypeError(
        #         "Only one argument can be used from:"
        #         " package_json, package_dict, package_name"
        #     )

        if package_json:
            self.content = package_json

        if package_dict:
            self.content = json.dumps(package_dict, indent=4)

        if package_name:
            self.content = get_package(package_name)

    def get_content(self):
        """Get current content of Record."""
        return self.content

    def validate(self):
        """Validate JSON record."""
        pass

    def to_string(self):
        """Convert content to string."""
        return json.dumps(self.content)

    def to_xml(self):
        """Convert content to XML record."""
        return convert_xml(self.content)

    def to_iso(self):
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

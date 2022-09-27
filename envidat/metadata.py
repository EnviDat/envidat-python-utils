"""Get EnviDat metadata records in various formats."""

import json
import logging
from typing import Literal, NoReturn, Union

from envidat.api.v1 import get_metadata_list_with_resources, get_package
from envidat.converters.bibtex_converter import convert_bibtex
from envidat.converters.datacite_converter import convert_datacite
from envidat.converters.dif_converter import convert_dif
from envidat.converters.iso_converter import convert_iso
from envidat.converters.ris_converter import convert_ris
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
        # Commented out line below because __init__ should return None
        # ) -> NoReturn:
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
            self.content = json.dumps(input_data, indent=4)

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

        # TODO refactor so that desired format is returned after
        # calling conversion functions below
        if extract:
            mapping = {
                "str": self.to_string,
                "xml": self.to_xml,
                "iso": self.to_iso,
            }
            mapping[extract]()
            # Commented out line below because it causes this error:
            # # TypeError: __init__() should return None, not 'str'
            # return self.get_content()

    # Removed expected return type of str in functions below
    # because sometimes self.content is also a dictionary

    def get_content(self):
        """Get current content of Record."""
        return self.content

    # TODO self.input is not an attribute
    def validate(self) -> bool:
        """Validate JSON record."""
        return validate_json(self.input)

    def to_string(self) -> str:
        """Convert content to string."""
        return json.dumps(self.content)

    def to_xml(self) -> str:
        """Convert content to XML record."""
        return convert_xml(self.content)

    def to_iso(self):
        """Convert content to ISO record."""
        return convert_iso(self.content)

    def to_ris(self):
        """Convert content to RIS format."""
        return convert_ris(self.content)

    def to_bibtex(self):
        """Convert content to BibTeX format."""
        return convert_bibtex(self.content)

    def to_dif(self):
        """Convert content to GCMD DIF 10.2 format."""
        return convert_dif(self.content)

    def to_datacite(self):
        """Convert content to DataCite format."""
        return convert_datacite(self.content)


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
            record_list.append(Record(input_data=json_entry).to_xml())
        elif as_iso:
            record_list.append(Record(input_data=json_entry).to_iso())
        else:
            record_list.append(Record(input_data=json_entry))
    return record_list

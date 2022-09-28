"""Get EnviDat metadata records in various formats."""

import json
import logging
from typing import Literal, NoReturn, Union

from envidat.api.v1 import (
    get_metadata_list_with_resources,
    get_metadata_name_doi,
    get_package,
)
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
        convert: Literal[
            "str", "xml", "iso", "bibtex", "dif", "datacite", "ris"
        ] = None,
    ) -> NoReturn:
        """
        Init the Record object.

        Only one argument should be passed for data format.

        Args:
            input_data [str, dict]: Data input, in JSON or dict form.
                Can also accept a package name to extract a record from the API.
            convert ["str", "xml", "iso", "bibtex", "dif", "datacite", "ris"]: Convert
                the content immediately to specified type.
        """
        if isinstance(input_data, dict):
            # Is dict
            log.debug("Dictionary input provided, reading as JSON")
            self.content = input_data

        elif isinstance(input_data, str):
            if validate_json(input_data):
                # Is JSON String, parse to JSON object/dict
                log.debug("Valid input JSON parsed")
                self.content = json.loads(input_data)
            else:
                # Get from API (JSON object/dict)
                log.debug("Attempting to get package JSON from API")
                self.content = dict(get_package(input_data))

        else:
            log.error("Input is not a valid type from (str,dict)")
            raise TypeError("Input must be of type string or dict")

        # Validate metadata record
        self.validate()

        if convert:
            mapping = {
                "json": self.to_json,
                "xml": self.to_xml,
                "iso": self.to_iso,
                "bibtex": self.to_bibtex,
                "dif": self.to_dif,
                "datacite": self.to_datacite,
                "ris": self.to_ris,
            }
            if convert == "datacite":
                name_doi_map = get_metadata_name_doi()
                self.content = mapping[convert](name_doi_map)
            else:
                self.content = mapping[convert]()

    def get_content(self):
        """Get current content of Record."""
        return self.content

    def validate(self) -> bool:
        """Validate metadata record."""
        metadata_keys = [
            "author",
            "author_email",
            "creator_user_id",
            "date",
            "doi",
            "funding",
            "id",
            "isopen",
            "language",
            "license_id",
            "license_title",
            "maintainer",
            "maintainer_email",
            "metadata_created",
            "metadata_modified",
            "name",
            "notes",
            "num_resources",
            "num_tags",
            "organization",
            "owner_org",
            "private",
            "publication",
            "publication_state",
            # "related_datasets", NOT ALWAYS PRESENT
            "related_publications",
            "resource_type",
            "resource_type_general",
            "spatial",
            "spatial_info",
            "state",
            "subtitle",
            "title",
            "type",
            "url",
            "version",
            "resources",
            "tags",
            "groups",
            "relationships_as_subject",
            "relationships_as_object",
        ]

        log.debug("Validating metadata record")
        if not isinstance(self.content, dict):
            log.error(f"Content is not a valid dictionary of metadata: {self.content}")
            raise ValueError("Content is not a valid dictionary of metadata.")

        missing_keys = list(set(metadata_keys) - set(self.content.keys()))
        if missing_keys:
            log.error(f"Metadata entry is missing fields: {missing_keys}")
            raise ValueError(
                "Content does not have all required fields for a metadata entry."
            )

        return True

    def to_json(self) -> str:
        """Convert content to JSON string."""
        return json.loads(self.content)

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

    def to_datacite(self, name_doi_map):
        """Convert content to DataCite format."""
        return convert_datacite(self.content, name_doi_map)


def get_all_metadata_record_list(
    convert: Literal["str", "xml", "iso", "bibtex", "dif", "datacite", "ris"] = None,
    content_only: bool = False,
) -> list:
    """
    Return all EnviDat metadata entries as Record objects.

    Defaults to standard Record, content in json format.

    Args:
        convert ["str", "xml", "iso", "bibtex", "dif", "datacite", "ris"]: Convert
            the content immediately to specified type.
        content_only (bool): Extract content from Record objects.

    Returns:
        list: Of Record entries for EnviDat metadata.
    """
    metadata = get_metadata_list_with_resources()
    record_list = []

    if convert == "datacite":
        name_doi_map = get_metadata_name_doi()

    for metadata_entry in metadata:
        record = Record(metadata_entry)

        if convert:
            mapping = {
                "json": record.to_json,
                "xml": record.to_xml,
                "iso": record.to_iso,
                "bibtex": record.to_bibtex,
                "dif": record.to_dif,
                "datacite": record.to_datacite,
                "ris": record.to_ris,
            }
            if convert == "datacite":
                record.content = mapping[convert](name_doi_map)
            else:
                record.content = mapping[convert]()

        if content_only:
            record_list.append(record.content)
        else:
            record_list.append(record)

    return record_list

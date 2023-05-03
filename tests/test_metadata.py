"""Tests for metadata Record."""

from collections import Counter

import pytest
from xmltodict import parse

from envidat.metadata import Record, get_all_metadata_record_list


def test_record_init_from_json(example_ckan_json, metadata_keys):
    """Test init using JSON input."""
    record = Record(example_ckan_json)

    assert Counter(list(record.content.keys())) == Counter(metadata_keys)


def test_record_init_from_dict(example_ckan_dict, metadata_keys):
    """Test init using dict input."""
    record = Record(example_ckan_dict)

    assert Counter(list(record.content.keys())) == Counter(metadata_keys)


def test_record_init_from_api(example_ckan_json, metadata_keys):
    """Test init using call to API."""
    record_from_api = Record("10-16904-3")

    assert Counter(list(record_from_api.content.keys())) == Counter(metadata_keys)

    record_from_json = Record(example_ckan_json)
    assert record_from_api.content == record_from_json.content


def test_record_init_with_validate(example_ckan_json, metadata_keys):
    """Test manual trigger of incorrect validation."""
    record = Record(example_ckan_json)

    is_valid = record.validate()
    assert is_valid

    record.content.pop("title")
    with pytest.raises(
        ValueError,
        match=("Content does not have all required fields for a metadata entry."),
    ):
        is_valid = record.validate()

    record.content = "not a valid json"
    with pytest.raises(
        ValueError, match="Content is not a valid dictionary of metadata."
    ):
        is_valid = record.validate()


def test_record_init_with_convert(example_ckan_json):
    """Test auto-conversion to another format during Record init."""
    record = Record(example_ckan_json)
    record_converted = Record(example_ckan_json, convert="xml")

    xml = record.to_xml()
    assert record_converted.content == xml


def test_get_all_metadata_record_list():
    """Test getting all metadata entries as list of Records."""
    metadata_records = get_all_metadata_record_list()

    assert len(metadata_records) > 500


def test_get_all_metadata_xml_list():
    """Test conversion of all Record contents to XML."""
    metadata_records = get_all_metadata_record_list(convert="xml")

    assert len(metadata_records) > 500
    assert type(metadata_records[0] is Record)


def test_get_all_metadata_iso_list_content_only():
    """Test converting and extracting contents only for each Record."""
    metadata_records = get_all_metadata_record_list(convert="iso", content_only=True)

    assert len(metadata_records) > 500
    assert type(metadata_records[0] is dict)


def test_get_all_metadata_datacite():
    """Test conversion of all to Datacite format, specific case."""
    metadata_records = get_all_metadata_record_list(convert="datacite")

    assert len(metadata_records) > 500


def test_get_single_dcat_ap_xml(example_ckan_json):
    """Test conversion of single Record to DCAT-AP format."""
    record = Record(example_ckan_json)
    record_converted = Record(example_ckan_json, convert="dcat-ap")

    xml = record.to_dcat_ap()
    assert record_converted.content == xml


def test_get_all_metadata_dcat_ap():
    """Test conversion of all to DCAT-AP format, specific case."""
    metadata_records = get_all_metadata_record_list(convert="dcat-ap")

    assert len(metadata_records) > 500


def test_get_all_metadata_dcat_ap_formatted_xml():
    """Test conversion of all to single DCAT-AP XML, specific case."""
    dcat_ap_xml = get_all_metadata_record_list(convert="dcat-ap", content_only=True)

    assert isinstance(dcat_ap_xml, str)

    dcat_dict = parse(dcat_ap_xml)
    assert list(dcat_dict.keys())[0] == "rdf:RDF"

    dataset_list = dcat_dict["rdf:RDF"]["dcat:Catalog"]["dcat:dataset"]
    assert len(dataset_list) > 500

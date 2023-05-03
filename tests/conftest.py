"""Configuration file for PyTest tests."""

import os
from tempfile import NamedTemporaryFile
from textwrap import dedent

import pytest
from moto import mock_s3

from envidat.api.v1 import get_metadata_name_doi
from envidat.converters.bibtex_converter import bibtex_convert_dataset
from envidat.converters.datacite_converter import datacite_convert_dataset
from envidat.converters.dcat_ap_converter import dcat_ap_convert_dataset
from envidat.converters.dif_converter import dif_convert_dataset
from envidat.converters.iso_converter import iso_convert_dataset
from envidat.converters.ris_converter import ris_convert_dataset
from envidat.s3.bucket import Bucket

os.environ["MOTO_ALLOW_NONEXISTENT_REGION"] = "True"


# @pytest.fixture(scope="session")
# def s3_env_vars():

#     # Disable region validation for moto
#     os.environ["MOTO_ALLOW_NONEXISTENT_REGION"] = "True"

#     # Official vars
#     os.environ["AWS_ACCESS_KEY_ID"] = "testing"
#     os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
#     os.environ["AWS_SECURITY_TOKEN"] = "testing"
#     os.environ["AWS_SESSION_TOKEN"] = "testing"
#     os.environ["AWS_DEFAULT_REGION"] = "testing"

#     # Custom vars
#     os.environ["AWS_ENDPOINT"] = "testing"
#     os.environ["AWS_ACCESS_KEY"] = "testing"
#     os.environ["AWS_SECRET_KEY"] = "testing"
#     os.environ["AWS_REGION"] = "testing"
#     os.environ["AWS_BUCKET_NAME"] = "testing"


@pytest.fixture(scope="session")
@mock_s3
def bucket():
    """Bucket for tests."""
    Bucket.config("testing", "testing", endpoint=None, region="testing")
    new_bucket = Bucket("testing")
    return new_bucket


@pytest.fixture(scope="session")
@mock_s3
def bucket2():
    """Second bucket when two are required in tests."""
    Bucket.config("testing", "testing", endpoint=None, region="testing")
    new_bucket = Bucket("testing2")
    return new_bucket


@pytest.fixture
def create_tempfile(scope="function"):
    """Create temporary file in tests."""

    def nested_tempfile(file_type, temp_dir=None, delete=True):
        """Nested temporary file within subdirectory."""
        temp_file = NamedTemporaryFile(
            dir=temp_dir, delete=delete, suffix=f".{file_type}"
        )
        with open(temp_file.name, "w", encoding="UTF-8") as f:
            f.write("test")
        return temp_file

    return nested_tempfile


@pytest.fixture
def bibtex_converter_one_package():
    """Single package in BibTeX format."""
    package_name = "bioclim_plus"
    file_format = "bibtex"
    extension = "bib"
    return bibtex_convert_dataset, package_name, file_format, extension


@pytest.fixture
def bibtex_converter_all_packages():
    """All packages in BibTeX format."""
    file_format = "bibtex"
    extension = "bib"
    return bibtex_convert_dataset, file_format, extension


#
@pytest.fixture
def datacite_converter_one_package():
    """Single package in Datacite format."""
    package_name = "gem2"
    file_format = "datacite"
    extension = "xml"
    return (
        datacite_convert_dataset,
        get_metadata_name_doi,
        package_name,
        file_format,
        extension,
    )


@pytest.fixture
def datacite_converter_all_packages():
    """All packages in Datacite format."""
    file_format = "datacite"
    extension = "xml"
    return datacite_convert_dataset, get_metadata_name_doi, file_format, extension


@pytest.fixture
def dif_converter_one_package():
    """Single package in Diff format."""
    package_name = "resolution-in-sdms-shapes-plant-multifaceted-diversity"
    file_format = "gcmd_dif"
    extension = "xml"
    return dif_convert_dataset, package_name, file_format, extension


@pytest.fixture
def dif_converter_all_packages():
    """All packages in Diff format."""
    file_format = "gcmd_dif"
    extension = "xml"
    return dif_convert_dataset, file_format, extension


@pytest.fixture
def iso_converter_one_package():
    """Single package in ISO format."""
    package_name = "intratrait"
    file_format = "iso19139"
    extension = "xml"
    return iso_convert_dataset, package_name, file_format, extension


@pytest.fixture
def iso_converter_all_packages():
    """All packages in ISO format."""
    file_format = "iso19139"
    extension = "xml"
    return iso_convert_dataset, file_format, extension


@pytest.fixture
def dcat_ap_converter_all_packages():
    """All packages in DCAT-AP format."""
    file_format = "dcat-ap-ch"
    extension = "xml"
    return dcat_ap_convert_dataset, file_format, extension


@pytest.fixture
def ris_converter_one_package():
    """Single package in RIS format."""
    package_name = "bioclim_plus"
    file_format = "ris"
    extension = "ris"
    return ris_convert_dataset, package_name, file_format, extension


@pytest.fixture
def ris_converter_all_packages():
    """All packages in RIS format."""
    file_format = "ris"
    extension = "ris"
    return ris_convert_dataset, file_format, extension


@pytest.fixture
def metadata_keys():
    """List of keys required for an EnviDat metadata Record."""
    return [
        "author",
        "author_email",
        "creator_user_id",
        "date",
        "doi",
        "extras",
        "funding",
        "id",
        "isopen",
        "language",
        "license_id",
        "license_title",
        "license_url",
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


@pytest.fixture
def example_ckan_dict():
    """CKAN metadata dict example for use in tests."""
    return {
        "author": '[{"name": "Phillips", "affiliation": "WSL Institute for snow and avalanche research SLF", "affiliation_03": "", "given_name": "Marcia", "identifier": "", "email": "phillips@slf.ch", "affiliation_02": ""}]',
        "author_email": None,
        "creator_user_id": "fe7fa798-2f5c-4ad3-b865-50260d7322cf",
        "date": '[{"date": "2013-04-15", "date_type": "collected", "end_date": ""}]',
        "doi": "",
        "funding": '[{"grant_number": "", "institution": "Funding information not available.", "institution_url": ""}]',
        "id": "7c4c3231-6903-45fc-a9a6-ddda5edb89a9",
        "isopen": True,
        "language": "en",
        "license_id": "odc-odbl",
        "license_title": "ODbL with Database Contents License (DbCL)",
        "license_url": "https://opendefinition.org/licenses/odc-odbl",
        "maintainer": '{"affiliation": "WSL Institute for snow and avalanche research SLF", "email": "phillips@slf.ch", "identifier": "", "given_name": "Marcia", "name": "Phillips"}',
        "maintainer_email": None,
        "metadata_created": "2016-11-07T16:16:40.621281",
        "metadata_modified": "2019-10-24T13:32:30.924354",
        "name": "gem2",
        "notes": "Meteorological station at Gemstock (3021 m asl) in Canton Uri. The station includes in/out LW/SW and a snow height sensor.",
        "num_resources": 1,
        "num_tags": 5,
        "organization": {
            "id": "e961ac74-4328-44c9-9c6e-93373a48464d",
            "name": "permafrost-and-snow-climatology",
            "title": "Permafrost",
            "type": "organization",
            "description": "Permanently frozen ground (so called permafrost) is widespread in the Alps above around 2500 m asl . Climate change can influence permafrost occurrence in several ways. The study of slope stability in ice-bearing permafrost features (e.g. rock glaciers, moraines) and of debris flows and rockfall in permafrost areas is becoming increasingly relevant due to the growing use of mountain areas for human activities. We investigate the interactions between permafrost, mountain infrastructure and the snow cover.",
            "image_url": "https://www.envidat.ch/uploads/group/2016-05-24-141521.837240logoslf.png",
            "created": "2018-11-15T15:28:01.425181",
            "is_organization": True,
            "approval_status": "approved",
            "state": "active",
        },
        "owner_org": "e961ac74-4328-44c9-9c6e-93373a48464d",
        "private": False,
        "publication": '{"publisher": "EnviDat", "publication_year": "2016"}',
        "publication_state": "",
        "related_publications": "",
        "resource_type": "Dataset",
        "resource_type_general": "dataset",
        "spatial": '{"type": "Point", "coordinates": [8.60904,46.60369]}',
        "spatial_info": "Gemsstock, Uri, Switzerland",
        "state": "active",
        "subtitle": "",
        "title": "GEM2: Meteorological and snow station at Gemsstock (3021 m asl), Canton Uri, Switzerland",
        "type": "dataset",
        "url": None,
        "version": "1.0",
        "extras": [{"key": "dora_link", "value": ""}],
        "resources": [
            {
                "cache_last_updated": None,
                "cache_url": None,
                "created": "2016-11-07T17:21:06.201532",
                "description": "Meteo data at Gemsstock  [Level 2 dataset](http://models.slf.ch/p/dataset-processing/).\r\n\r\nfields           = timestamp TSS HS VW DW VW_MAX OSWR ISWR ILWR RECORD AUX_VOLTAGE LOGGER_VOLTAGE LW_SENSOR_TEMP VENTILATION_FLAG OLWR",
                "doi": "",
                "format": "SMET",
                "hash": "",
                "id": "658cf67d-b337-4837-a511-40059ab52471",
                "last_modified": "2016-11-07T16:21:06.155704",
                "metadata_modified": None,
                "mimetype": None,
                "mimetype_inner": None,
                "name": "DATA ACCESS",
                "package_id": "7c4c3231-6903-45fc-a9a6-ddda5edb89a9",
                "position": 0,
                "resource_type": None,
                "restricted": '{"level": "public", "allowed_users": ""}',
                "size": None,
                "state": "active",
                "url": "http://montblanc.slf.ch/DPS/dat/GEM2_L2.smet",
                "url_type": "",
            }
        ],
        "tags": [
            {
                "display_name": "GEMSTOCK",
                "id": "b9cf4960-d146-42c5-811e-cdf2bd8a4546",
                "name": "GEMSTOCK",
                "state": "active",
                "vocabulary_id": None,
            },
            {
                "display_name": "LONGWAVE RADIATION",
                "id": "4a3b1721-1050-434e-8573-9c36284bb50c",
                "name": "LONGWAVE RADIATION",
                "state": "active",
                "vocabulary_id": None,
            },
            {
                "display_name": "METEO STATION",
                "id": "92a24e76-037b-4a44-8851-1fa52a64b689",
                "name": "METEO STATION",
                "state": "active",
                "vocabulary_id": None,
            },
            {
                "display_name": "SHORTWAVE RADIATION",
                "id": "2a295030-e71a-4fe6-87b0-5edfb1603c1b",
                "name": "SHORTWAVE RADIATION",
                "state": "active",
                "vocabulary_id": None,
            },
            {
                "display_name": "SNOW HEIGHT",
                "id": "6bdc807f-58d4-4e65-8b9c-b0e33bbfb694",
                "name": "SNOW HEIGHT",
                "state": "active",
                "vocabulary_id": None,
            },
        ],
        "groups": [],
        "relationships_as_subject": [],
        "relationships_as_object": [],
    }


@pytest.fixture
def example_ckan_json():
    """CKAN metadata JSON example for use in tests."""
    return dedent(
        r"""
        {
        "author": "[{\"name\": \"Phillips\", \"affiliation\": \"WSL Institute for snow and avalanche research SLF\", \"affiliation_03\": \"\", \"given_name\": \"Marcia\", \"identifier\": \"\", \"email\": \"phillips@slf.ch\", \"affiliation_02\": \"\"}]",
        "author_email": null,
        "creator_user_id": "fe7fa798-2f5c-4ad3-b865-50260d7322cf",
        "date": "[{\"date\": \"2013-04-15\", \"date_type\": \"collected\", \"end_date\": \"\"}]",
        "doi": "",
        "funding": "[{\"grant_number\": \"\", \"institution\": \"Funding information not available.\", \"institution_url\": \"\"}]",
        "id": "7c4c3231-6903-45fc-a9a6-ddda5edb89a9",
        "isopen": true,
        "language": "en",
        "license_id": "odc-odbl",
        "license_title": "ODbL with Database Contents License (DbCL)",
        "license_url": "https://opendefinition.org/licenses/odc-odbl",
        "maintainer": "{\"affiliation\": \"WSL Institute for snow and avalanche research SLF\", \"email\": \"phillips@slf.ch\", \"identifier\": \"\", \"given_name\": \"Marcia\", \"name\": \"Phillips\"}",
        "maintainer_email": null,
        "metadata_created": "2016-11-07T16:16:40.621281",
        "metadata_modified": "2019-10-24T13:32:30.924354",
        "name": "gem2",
        "notes": "Meteorological station at Gemstock (3021 m asl) in Canton Uri. The station includes in/out LW/SW and a snow height sensor.",
        "num_resources": 1,
        "num_tags": 5,
        "organization": {
            "id": "e961ac74-4328-44c9-9c6e-93373a48464d",
            "name": "permafrost-and-snow-climatology",
            "title": "Permafrost",
            "type": "organization",
            "description": "Permanently frozen ground (so called permafrost) is widespread in the Alps above around 2500 m asl . Climate change can influence permafrost occurrence in several ways. The study of slope stability in ice-bearing permafrost features (e.g. rock glaciers, moraines) and of debris flows and rockfall in permafrost areas is becoming increasingly relevant due to the growing use of mountain areas for human activities. We investigate the interactions between permafrost, mountain infrastructure and the snow cover.",
            "image_url": "https://www.envidat.ch/uploads/group/2016-05-24-141521.837240logoslf.png",
            "created": "2018-11-15T15:28:01.425181",
            "is_organization": true,
            "approval_status": "approved",
            "state": "active"
        },
        "owner_org": "e961ac74-4328-44c9-9c6e-93373a48464d",
        "private": false,
        "publication": "{\"publisher\": \"EnviDat\", \"publication_year\": \"2016\"}",
        "publication_state": "",
        "related_publications": "",
        "resource_type": "Dataset",
        "resource_type_general": "dataset",
        "spatial": "{\"type\": \"Point\", \"coordinates\": [8.60904,46.60369]}",
        "spatial_info": "Gemsstock, Uri, Switzerland",
        "state": "active",
        "subtitle": "",
        "title": "GEM2: Meteorological and snow station at Gemsstock (3021 m asl), Canton Uri, Switzerland",
        "type": "dataset",
        "url": null,
        "version": "1.0",
        "extras": [
            {
            "key": "dora_link",
            "value": ""
            }
        ],
        "resources": [
            {
            "cache_last_updated": null,
            "cache_url": null,
            "created": "2016-11-07T17:21:06.201532",
            "description": "Meteo data at Gemsstock  [Level 2 dataset](http://models.slf.ch/p/dataset-processing/).\r\n\r\nfields           = timestamp TSS HS VW DW VW_MAX OSWR ISWR ILWR RECORD AUX_VOLTAGE LOGGER_VOLTAGE LW_SENSOR_TEMP VENTILATION_FLAG OLWR",
            "doi": "",
            "format": "SMET",
            "hash": "",
            "id": "658cf67d-b337-4837-a511-40059ab52471",
            "last_modified": "2016-11-07T16:21:06.155704",
            "metadata_modified": null,
            "mimetype": null,
            "mimetype_inner": null,
            "name": "DATA ACCESS",
            "package_id": "7c4c3231-6903-45fc-a9a6-ddda5edb89a9",
            "position": 0,
            "resource_type": null,
            "restricted": "{\"level\": \"public\", \"allowed_users\": \"\"}",
            "size": null,
            "state": "active",
            "url": "http://montblanc.slf.ch/DPS/dat/GEM2_L2.smet",
            "url_type": ""
            }
        ],
        "tags": [
            {
            "display_name": "GEMSTOCK",
            "id": "b9cf4960-d146-42c5-811e-cdf2bd8a4546",
            "name": "GEMSTOCK",
            "state": "active",
            "vocabulary_id": null
            },
            {
            "display_name": "LONGWAVE RADIATION",
            "id": "4a3b1721-1050-434e-8573-9c36284bb50c",
            "name": "LONGWAVE RADIATION",
            "state": "active",
            "vocabulary_id": null
            },
            {
            "display_name": "METEO STATION",
            "id": "92a24e76-037b-4a44-8851-1fa52a64b689",
            "name": "METEO STATION",
            "state": "active",
            "vocabulary_id": null
            },
            {
            "display_name": "SHORTWAVE RADIATION",
            "id": "2a295030-e71a-4fe6-87b0-5edfb1603c1b",
            "name": "SHORTWAVE RADIATION",
            "state": "active",
            "vocabulary_id": null
            },
            {
            "display_name": "SNOW HEIGHT",
            "id": "6bdc807f-58d4-4e65-8b9c-b0e33bbfb694",
            "name": "SNOW HEIGHT",
            "state": "active",
            "vocabulary_id": null
            }
        ],
        "groups": [],
        "relationships_as_subject": [],
        "relationships_as_object": []
        }"""
    ).strip()

"""Configuration file for PyTest tests."""

import os
from tempfile import NamedTemporaryFile
from textwrap import dedent

import pytest
from moto import mock_s3

from envidat.converters.bibtex_converter import bibtex_convert_dataset
from envidat.converters.datacite_converter import convert_datacite
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
    package_name = "10-16904-3"
    file_format = "datacite"
    extension = "xml"
    return (
        convert_datacite,
        package_name,
        file_format,
        extension,
    )


@pytest.fixture
def datacite_converter_all_packages():
    """All packages in Datacite format."""
    file_format = "datacite"
    extension = "xml"
    return convert_datacite, file_format, extension


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
        # "language",
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
        "author": '[{"name": "Müller", "affiliation": "WSL", "affiliation_03": "", "given_name": "Kalin", "identifier": "", "email": "kalin.müller@wsl.ch", "affiliation_02": ""}, {"name": "Fraefel", "affiliation": "WSL", "affiliation_03": "", "given_name": "Marielle", "identifier": "", "email": "marielle.fraefel@wsl.ch", "affiliation_02": ""}, {"name": "Cioldi", "affiliation": "WSL", "affiliation_03": "", "given_name": "Fabrizio", "identifier": "", "email": "fabrizio.cioldi@wsl.ch", "affiliation_02": ""}, {"name": "Camin", "affiliation": "FOEN", "affiliation_03": "", "affiliation_02": "", "identifier": "", "email": "paolo.camin@bafu.admin.ch", "given_name": "Paolo"}, {"name": "Fischer", "affiliation": "WSL", "affiliation_03": "", "affiliation_02": "", "identifier": "", "email": "christoph.fischer@wsl.ch", "given_name": "Christoph"}]',
        "author_email": None,
        "creator_user_id": "334cee1e-6afa-4639-88a2-f980e6ff42c3",
        "date": '[{"date": "2013-01-01", "date_type": "collected", "end_date": ""}]',
        "doi": "10.16904/3",
        "funding": '[{"grant_number": "", "institution": "Federal Office for the Environment FOEN", "institution_url": ""}]',
        "id": "99105534-4a3d-4062-a4f9-69933eab4d37",
        "isopen": False,
        "license_id": "wsl-data",
        "license_title": "WSL Data Policy",
        "license_url": "https://www.wsl.ch/en/about-wsl/programmes-and-initiatives/envidat.html",
        "maintainer": '{"affiliation": "WSL", "email": "fabrizio.cioldi@wsl.ch", "identifier": "", "given_name": "Fabrizio", "name": "Cioldi"}',
        "maintainer_email": None,
        "metadata_created": "2016-10-16T22:24:05.567182",
        "metadata_modified": "2019-10-31T22:59:07.778166",
        "name": "10-16904-3",
        "notes": "In 2013–2014, a survey was conducted in Switzerland to update the Forest Access Roads geo-dataset within the framework of the Swiss National Forest Inventory (NFI). The resulting nationwide dataset contains valuable information on truck-accessible forest roads that can be used to transport wood. The survey involved interviewing staff from the approximately 800 local forest services in Switzerland and recording the data first on paper maps and then in digitized form. The data in the NFI on the forest roads could thus be updated and additional information regarding their trafficability for specific categories of truck included. The information has now been attached to the geometries of the Roads and Tracks of the swissTLM3D (release 2012) of the Federal Office of Topography swisstopo. The resulting data are suitable for statistical analyses and modeling, but further (labour-intensive) validation work would be necessary if they are to be used as a basis for applications requiring more spatial accuracy, such as navigation systems. The data are managed at the Swiss Federal Institute for Forest, Snow and Landscape Research (WSL) and are available for third parties for non-commercial use provided they have purchased a TLM license. \r\n\r\n__Related Publication__: [doi: 10.3188/szf.2016.0136](http://dx.doi.org/10.3188/szf.2016.0136)",
        "num_resources": 1,
        "num_tags": 5,
        "organization": {
            "id": "49192b11-adac-4e68-ad64-be15a4321347",
            "name": "nfi",
            "title": "NFI",
            "type": "organization",
            "description": "The Swiss National Forest Inventory records the current state and the changes of the Swiss forest. The survey obtains data about trees, stands, sample plots and through enquiries at the local forest service.\r\n\r\nThe NFI carried out by the Swiss Federal Institute for Forest, Snow and Landscape Research (WSL) in collaboration with the Forest Division at Federal Office for the Environment (FOEN ). The WSL is responsible for the planning, survey and analysis, as well as the scientific interpretation and publication of the NFI. The political interpretation and implementation is done by the Forest Division.\r\n\r\nThe first survey (LFI1) took place from 1983–85, the second survey followed in 1993–95 and the third inventory was carried out 2004–2006. Since 2009, the continuous survey of the fourth NFI (2009–2017) has been in progress.\r\n\r\nMore information: https://www.lfi.ch/lfi/lfi-en.php",
            "image_url": "https://www.lfi.ch/layout/images/logo.gif",
            "created": "2016-07-05T13:46:14.456454",
            "is_organization": True,
            "approval_status": "approved",
            "state": "active",
        },
        "owner_org": "49192b11-adac-4e68-ad64-be15a4321347",
        "private": False,
        "publication": '{"publisher": "Swiss Federal Institute for Forest, Snow and Landscape WSL /  Federal Office for the Environment FOEN ", "publication_year": "2016"}',
        "publication_state": "published",
        "related_publications": "",
        "resource_type": "Dataset",
        "resource_type_general": "dataset",
        "spatial": '{"type": "Polygon", "coordinates": [[[5.95587, 45.81802],[5.95587, 47.80838],[10.49203, 47.80838],[10.49203, 45.81802],[5.95587, 45.81802]]]}',
        "spatial_info": "Switzerland [45.81802 5.95587 47.80838 10.49203]",
        "state": "active",
        "subtitle": "",
        "title": "Forest Access Roads 2013",
        "type": "dataset",
        "url": None,
        "version": "1",
        "extras": [{"key": "dora_link", "value": ""}],
        "resources": [
            {
                "cache_last_updated": None,
                "cache_url": None,
                "created": "2016-10-17T00:26:11.582643",
                "description": "Article describing the dataset, as well as its acquisition and potential uses.\r\nTo access the data please contact Fabrizio Cioldi.",
                "doi": "10.3188/szf.2016.0136",
                "format": "URL",
                "hash": "",
                "id": "72e5616c-5d4d-4aa7-8702-e8d58c3d6f9f",
                "last_modified": None,
                "metadata_modified": None,
                "mimetype": "application/pdf",
                "mimetype_inner": None,
                "name": "Publication Walderschliessungsstrassen 2013",
                "package_id": "99105534-4a3d-4062-a4f9-69933eab4d37",
                "position": 0,
                "resource_type": None,
                "restricted": '{"level": "public", "allowed_users": ""}',
                "size": None,
                "state": "active",
                "url": "https://www.dora.lib4ri.ch/wsl/islandora/object/wsl:5563",
                "url_type": "",
            }
        ],
        "tags": [
            {
                "display_name": "FOREST ACCESS ROADS",
                "id": "aa4c7d84-f08d-4a8a-aeb0-c2e2adbd5982",
                "name": "FOREST ACCESS ROADS",
                "state": "active",
                "vocabulary_id": None,
            },
            {
                "display_name": "FOREST TRANSPORTATION SYSTEMS",
                "id": "2d33b726-2878-480e-8210-0d82271edde2",
                "name": "FOREST TRANSPORTATION SYSTEMS",
                "state": "active",
                "vocabulary_id": None,
            },
            {
                "display_name": "TIMBER HARVESTING",
                "id": "d677b7e0-748e-49cf-8049-bff0d08644d0",
                "name": "TIMBER HARVESTING",
                "state": "active",
                "vocabulary_id": None,
            },
            {
                "display_name": "TRAFFICABILITY",
                "id": "d9003596-a5d9-4eac-91aa-b31d2743a44a",
                "name": "TRAFFICABILITY",
                "state": "active",
                "vocabulary_id": None,
            },
            {
                "display_name": "TRUCKS",
                "id": "3815dcbd-db09-46cb-80da-ca01ba415af5",
                "name": "TRUCKS",
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
        "author": "[{\"name\": \"Müller\", \"affiliation\": \"WSL\", \"affiliation_03\": \"\", \"given_name\": \"Kalin\", \"identifier\": \"\", \"email\": \"kalin.müller@wsl.ch\", \"affiliation_02\": \"\"}, {\"name\": \"Fraefel\", \"affiliation\": \"WSL\", \"affiliation_03\": \"\", \"given_name\": \"Marielle\", \"identifier\": \"\", \"email\": \"marielle.fraefel@wsl.ch\", \"affiliation_02\": \"\"}, {\"name\": \"Cioldi\", \"affiliation\": \"WSL\", \"affiliation_03\": \"\", \"given_name\": \"Fabrizio\", \"identifier\": \"\", \"email\": \"fabrizio.cioldi@wsl.ch\", \"affiliation_02\": \"\"}, {\"name\": \"Camin\", \"affiliation\": \"FOEN\", \"affiliation_03\": \"\", \"affiliation_02\": \"\", \"identifier\": \"\", \"email\": \"paolo.camin@bafu.admin.ch\", \"given_name\": \"Paolo\"}, {\"name\": \"Fischer\", \"affiliation\": \"WSL\", \"affiliation_03\": \"\", \"affiliation_02\": \"\", \"identifier\": \"\", \"email\": \"christoph.fischer@wsl.ch\", \"given_name\": \"Christoph\"}]",
        "author_email": null,
        "creator_user_id": "334cee1e-6afa-4639-88a2-f980e6ff42c3",
        "date": "[{\"date\": \"2013-01-01\", \"date_type\": \"collected\", \"end_date\": \"\"}]",
        "doi": "10.16904/3",
        "funding": "[{\"grant_number\": \"\", \"institution\": \"Federal Office for the Environment FOEN\", \"institution_url\": \"\"}]",
        "id": "99105534-4a3d-4062-a4f9-69933eab4d37",
        "isopen": false,
        "license_id": "wsl-data",
        "license_title": "WSL Data Policy",
        "license_url": "https://www.wsl.ch/en/about-wsl/programmes-and-initiatives/envidat.html",
        "maintainer": "{\"affiliation\": \"WSL\", \"email\": \"fabrizio.cioldi@wsl.ch\", \"identifier\": \"\", \"given_name\": \"Fabrizio\", \"name\": \"Cioldi\"}",
        "maintainer_email": null,
        "metadata_created": "2016-10-16T22:24:05.567182",
        "metadata_modified": "2019-10-31T22:59:07.778166",
        "name": "10-16904-3",
        "notes": "In 2013–2014, a survey was conducted in Switzerland to update the Forest Access Roads geo-dataset within the framework of the Swiss National Forest Inventory (NFI). The resulting nationwide dataset contains valuable information on truck-accessible forest roads that can be used to transport wood. The survey involved interviewing staff from the approximately 800 local forest services in Switzerland and recording the data first on paper maps and then in digitized form. The data in the NFI on the forest roads could thus be updated and additional information regarding their trafficability for specific categories of truck included. The information has now been attached to the geometries of the Roads and Tracks of the swissTLM3D (release 2012) of the Federal Office of Topography swisstopo. The resulting data are suitable for statistical analyses and modeling, but further (labour-intensive) validation work would be necessary if they are to be used as a basis for applications requiring more spatial accuracy, such as navigation systems. The data are managed at the Swiss Federal Institute for Forest, Snow and Landscape Research (WSL) and are available for third parties for non-commercial use provided they have purchased a TLM license. \r\n\r\n__Related Publication__: [doi: 10.3188/szf.2016.0136](http://dx.doi.org/10.3188/szf.2016.0136)",
        "num_resources": 1,
        "num_tags": 5,
        "organization": {
            "id": "49192b11-adac-4e68-ad64-be15a4321347",
            "name": "nfi",
            "title": "NFI",
            "type": "organization",
            "description": "The Swiss National Forest Inventory records the current state and the changes of the Swiss forest. The survey obtains data about trees, stands, sample plots and through enquiries at the local forest service.\r\n\r\nThe NFI carried out by the Swiss Federal Institute for Forest, Snow and Landscape Research (WSL) in collaboration with the Forest Division at Federal Office for the Environment (FOEN ). The WSL is responsible for the planning, survey and analysis, as well as the scientific interpretation and publication of the NFI. The political interpretation and implementation is done by the Forest Division.\r\n\r\nThe first survey (LFI1) took place from 1983–85, the second survey followed in 1993–95 and the third inventory was carried out 2004–2006. Since 2009, the continuous survey of the fourth NFI (2009–2017) has been in progress.\r\n\r\nMore information: https://www.lfi.ch/lfi/lfi-en.php",
            "image_url": "https://www.lfi.ch/layout/images/logo.gif",
            "created": "2016-07-05T13:46:14.456454",
            "is_organization": true,
            "approval_status": "approved",
            "state": "active"
        },
        "owner_org": "49192b11-adac-4e68-ad64-be15a4321347",
        "private": false,
        "publication": "{\"publisher\": \"Swiss Federal Institute for Forest, Snow and Landscape WSL /  Federal Office for the Environment FOEN \", \"publication_year\": \"2016\"}",
        "publication_state": "published",
        "related_publications": "",
        "resource_type": "Dataset",
        "resource_type_general": "dataset",
        "spatial": "{\"type\": \"Polygon\", \"coordinates\": [[[5.95587, 45.81802],[5.95587, 47.80838],[10.49203, 47.80838],[10.49203, 45.81802],[5.95587, 45.81802]]]}",
        "spatial_info": "Switzerland [45.81802 5.95587 47.80838 10.49203]",
        "state": "active",
        "subtitle": "",
        "title": "Forest Access Roads 2013",
        "type": "dataset",
        "url": null,
        "version": "1",
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
            "created": "2016-10-17T00:26:11.582643",
            "description": "Article describing the dataset, as well as its acquisition and potential uses.\r\nTo access the data please contact Fabrizio Cioldi.",
            "doi": "10.3188/szf.2016.0136",
            "format": "URL",
            "hash": "",
            "id": "72e5616c-5d4d-4aa7-8702-e8d58c3d6f9f",
            "last_modified": null,
            "metadata_modified": null,
            "mimetype": "application/pdf",
            "mimetype_inner": null,
            "name": "Publication Walderschliessungsstrassen 2013",
            "package_id": "99105534-4a3d-4062-a4f9-69933eab4d37",
            "position": 0,
            "resource_type": null,
            "restricted": "{\"level\": \"public\", \"allowed_users\": \"\"}",
            "size": null,
            "state": "active",
            "url": "https://www.dora.lib4ri.ch/wsl/islandora/object/wsl:5563",
            "url_type": ""
            }
        ],
        "tags": [
            {
            "display_name": "FOREST ACCESS ROADS",
            "id": "aa4c7d84-f08d-4a8a-aeb0-c2e2adbd5982",
            "name": "FOREST ACCESS ROADS",
            "state": "active",
            "vocabulary_id": null
            },
            {
            "display_name": "FOREST TRANSPORTATION SYSTEMS",
            "id": "2d33b726-2878-480e-8210-0d82271edde2",
            "name": "FOREST TRANSPORTATION SYSTEMS",
            "state": "active",
            "vocabulary_id": null
            },
            {
            "display_name": "TIMBER HARVESTING",
            "id": "d677b7e0-748e-49cf-8049-bff0d08644d0",
            "name": "TIMBER HARVESTING",
            "state": "active",
            "vocabulary_id": null
            },
            {
            "display_name": "TRAFFICABILITY",
            "id": "d9003596-a5d9-4eac-91aa-b31d2743a44a",
            "name": "TRAFFICABILITY",
            "state": "active",
            "vocabulary_id": null
            },
            {
            "display_name": "TRUCKS",
            "id": "3815dcbd-db09-46cb-80da-ca01ba415af5",
            "name": "TRUCKS",
            "state": "active",
            "vocabulary_id": null
            }
        ],
        "groups": [],
        "relationships_as_subject": [],
        "relationships_as_object": []
        }"""
    ).strip()

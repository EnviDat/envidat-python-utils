"""Configuration file for PyTest tests."""

import os
from tempfile import NamedTemporaryFile

import pytest
from moto import mock_s3

from envidat.api.v1 import get_metadata_name_doi
from envidat.converters.bibtex_converter import bibtex_convert_dataset
from envidat.converters.datacite_converter import datacite_convert_dataset
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
    package_name = (
        "ecological-properties-of-urban-ecosystems-biodiversity-dataset-of-zurich"
    )
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

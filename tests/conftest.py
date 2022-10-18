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
        "related_datasets",
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
        "author": '[{"name": "Casanelles-Abella", "data_credit": ["validation", "curation", "software", "publication"], "affiliation": "Conservation Biology, Biodiversity and Conservation Biology, Swiss Federal Institute for Forest, Snow and Landscape Research WSL, 8903 Birmensdorf, Switzerland", "affiliation_03": "", "affiliation_02": "Landscape Ecology, Institute of Terrestrial Ecosystems, ETH Z\\u00fcrich, 8049 Z\\u00fcrich, Switzerland", "identifier": "0000-0003-1924-9298", "email": "joan.casanelles@wsl.ch", "given_name": "Joan"}, {"name": "Chauvier", "data_credit": ["software", "publication"], "email": "yohann.chauvier@wsl.ch", "affiliation": "Dynamic Macroecology, Landscape Change Science, Swiss Federal Institute for Forest, Snow and Landscape Research WSL, 8903 Birmensdorf, Switzerland", "affiliation_03": "", "given_name": "Yohann", "identifier": "0000-0001-9399-3192", "affiliation_02": ""}, {"name": "Zellweger", "data_credit": ["software", "publication"], "email": "florian.zellweger@wsl.ch", "affiliation": "Resource Analysis, Forest Resource and Management, Swiss Federal Institute for Forest, Snow and Landscape Research WSL, 8903 Birmensdorf, Switzerland", "affiliation_03": "", "affiliation_02": "", "identifier": "0000-0003-1265-9147", "given_name": "Florian"}, {"name": "Villiger", "data_credit": ["software", "publication"], "affiliation": "Landscape Ecology, Institute of Terrestrial Ecosystems, ETH Z\\u00fcrich, 8049 Z\\u00fcrich, Switzerland", "affiliation_03": "", "given_name": "Petrissa", "identifier": "", "email": "villigep@student.ethz.ch", "affiliation_02": ""}, {"name": "Frey", "data_credit": ["software", "publication"], "affiliation": "Conservation Biology, Biodiversity and Conservation Biology, Swiss Federal Institute for Forest, Snow and Landscape Research WSL, 8903 Birmensdorf, Switzerland", "affiliation_03": "", "affiliation_02": "Spatial Evolutionary Ecology, Biodiversity and Conservation Biology, Swiss Federal Institute for Forest, Snow and Landscape Research WSL, 8903 Birmensdorf, Switzerland", "identifier": "0000-0002-4603-0438", "email": "david.frey@wsl.ch", "given_name": "David Johannes"}, {"name": "Ginzler", "data_credit": ["software", "publication"], "affiliation": "Remote Sensing, Landscape Change Science, Swiss Federal Institute for Forest, Snow and Landscape Research WSL, 8903 Birmensdorf, Switzerland", "affiliation_03": "", "affiliation_02": "", "identifier": "0000-0001-6365-2151", "email": "christian.ginzler@wsl.ch", "given_name": "Christian"}, {"name": "Moretti", "data_credit": ["collection", "publication", "supervision"], "email": "marco.moretti@wsl.ch", "affiliation": "Conservation Biology, Biodiversity and Conservation Biology, Swiss Federal Institute for Forest, Snow and Landscape Research WSL, 8903 Birmensdorf, Switzerland", "affiliation_03": "", "given_name": "Marco", "identifier": "0000-0002-5845-3198", "affiliation_02": ""}, {"name": "Pellissier", "data_credit": ["publication", "supervision"], "affiliation": "Landscape Ecology, Institute of Terrestrial Ecosystems, ETH Z\\u00fcrich, 8049 Z\\u00fcrich, Switzerland", "affiliation_03": "", "given_name": "Loic", "identifier": "0000-0002-2289-8259", "email": "loic.pellissier@wsl.ch", "affiliation_02": "Landscape Ecology, Landscape Change Science, Swiss Federal Institute for Forest, Snow and Landscape Research WSL, 8903 Birmensdorf, Switzerland"}]',
        "author_email": None,
        "creator_user_id": "c7314170-c2ac-46d6-9193-eee220229e8b",
        "date": '[{"date": "01.08.2006", "date_type": "collected", "end_date": "16.09.2007"}, {"date": "25.05.2010", "date_type": "collected", "end_date": "03.09.2010"}, {"date": "06.01.2015", "date_type": "collected", "end_date": "20.09.2016"}, {"date": "2017-02-01", "date_type": "collected", "end_date": "2017-10-31"}]',
        "doi": "10.16904/envidat.172",
        "funding": '[{"grant_number": "H2020, BiodivERsA32015104", "institution": "Swiss National Science Foundation (project 31BD30_172467) within the programme ERA-Net BiodivERsA project “BioVEINS: Connectivity of green and blue infrastructures: living veins for biodiverse and healthy cities” (H2020 BiodivERsA32015104)", "institution_url": "http://bioveins.eu, https://www.biodiversa.org, http://p3.snf.ch/project-172467"}, {"grant_number": "172198", "institution": "F.Z. received funding from the Swiss National Science Foundation (project 172198)", "institution_url": "http://p3.snf.ch/project-172198"}, {"grant_number": "310030L_170059", "institution": "Y.C. acknowledges the ANR-SNF bilateral project OriginAlps (grant number 310030L_170059)", "institution_url": "http://p3.snf.ch/project-170059"}]',
        "id": "0f81429a-204e-4720-929e-5b251e9ab1c4",
        "isopen": False,
        "language": "en",
        "license_id": "other-undefined",
        "license_title": "Other (Specified in the description)",
        "maintainer": '{"affiliation": "Conservation Biology, Biodiversity and Conservation Biology, Swiss Federal Institute for Forest, Snow and Landscape Research WSL, 8903 Birmensdorf, Switzerland", "email": "marco.moretti@wsl.ch", "name": "Moretti", "identifier": "0000-0002-5845-3198", "given_name": "Marco"}',
        "maintainer_email": None,
        "metadata_created": "2020-09-07T15:14:02.051289",
        "metadata_modified": "2020-09-17T09:14:48.641088",
        "name": "ecological-properties-of-urban-ecosystems-biodiversity-dataset-of-zurich",
        "notes": "Richness, site occurrence and abundance data of bees, beetles, birds, hoverflies, net-wingeds, true bugs, snails, spiders, milipides, wasps collected in the city of Zurich using different sampling techniques, and the environmental variables for each sampling site.\r\nData are provided on request to contact person against bilateral agreement.",
        "num_resources": 5,
        "num_tags": 11,
        "organization": {
            "id": "32672ec5-c180-471e-92f7-ef58e00eb1fb",
            "name": "conservation-biology",
            "title": "Conservation Biology",
            "type": "organization",
            "description": "We study the relationship between threatened species and their habitat with the objective to develop evidence-based instruments for conservation. The viability of populations of habitat specialists is often limited due to restricted availability of suitable habitat or discontinuous distribution. We focus on selected animal species of conservation concern (forest birds, bats, forest insects) and analyse species-habitat relationships at a scale ranging from single subpopulations to entire metapopulations. We strive towards standardised recording of elusive species with novel techniques, assessing environmental variables and combining these field data with data from remote sensing. We determine limiting factors (habitat, climate, resources) and predict species occurrence and habitat suitability with modelling techniques.\r\n\r\nThese models allow to predict species occurrence patterns and to delineate evidence-based priority areas for conservation. Our long-term collaboration with federal and cantonal stakeholders of forest and nature conservation enables the combination of research results with conservation requirements (e.g. species action plans, forest biodiversity expert panel, scientific counsel for bat protection). While we investigate complete distribution ranges in bats, we focus on forest habitats in birds and insects given the large extent and high importance of forests for biodiversity conservation in Switzerland.",
            "image_url": "2018-07-10-090115.162284LogoWSL.svg",
            "created": "2018-05-18T09:12:30.577470",
            "is_organization": True,
            "approval_status": "approved",
            "state": "active",
        },
        "owner_org": "32672ec5-c180-471e-92f7-ef58e00eb1fb",
        "private": False,
        "publication": '{"publisher": "EnviDat", "publication_year": "2020"}',
        "publication_state": "published",
        "related_datasets": "* Dataset_1_SAD_SOD.txt\r\n* Dataset_2_SDM_data.txt\r\n* Dataset_3_Species_richness_hyper.txt\r\n* Dataset_4_Species_richness_rare.txt\r\n* Dataset_5_Species_richness_all.txt\r\n*\r\nData extracts in TAB-delimted format. First row is header",
        "related_publications": "",
        "resource_type": "dataset",
        "resource_type_general": "dataset",
        "spatial": '{"type":"Polygon","coordinates":[[[8.463935852050781,47.329748306633896],[8.463935852050781,47.427622733649606],[8.602638244628906,47.427622733649606],[8.602638244628906,47.329748306633896],[8.463935852050781,47.329748306633896]]]}',
        "spatial_info": "Switzerland",
        "state": "active",
        "subtitle": "",
        "title": "Ecological properties of urban ecosystems. Biodiversity dataset of Zurich",
        "type": "dataset",
        "url": None,
        "version": "1.0",
        "resources": [
            {
                "cache_last_updated": None,
                "cache_url": None,
                "created": "2020-09-07T15:18:31.256479",
                "description": "abundance and occurrence data of the 1446 species studied, used to investigate species-abundance distributions and species-occurrence distributions",
                "doi": "",
                "format": "TXT",
                "hash": "",
                "id": "a7a96a85-dc46-4b5f-bcf4-4d91485e3d03",
                "last_modified": "2020-09-07T15:18:31.071900",
                "metadata_modified": None,
                "mimetype": "text/plain",
                "mimetype_inner": None,
                "name": "Dataset_1_SAD_SOD.txt",
                "package_id": "0f81429a-204e-4720-929e-5b251e9ab1c4",
                "position": 0,
                "resource_size": '{"size_value": "", "size_units": "kb"}',
                "resource_type": None,
                "restricted": '{"shared_secret": "", "allowed_users": "marco_moretti-wsl_ch,joan_casanelles-wsl_ch", "level": "same_organization"}',
                "size": 73478,
                "state": "active",
                "url": "https://www.envidat.ch/dataset/0f81429a-204e-4720-929e-5b251e9ab1c4/resource/a7a96a85-dc46-4b5f-bcf4-4d91485e3d03/download/dataset_1_sad_sod.txt",
                "url_type": "upload",
            },
            {
                "cache_last_updated": None,
                "cache_url": None,
                "created": "2020-09-07T15:19:36.603618",
                "description": "contains the raw data to perform species distribution models, only for common species",
                "doi": "",
                "format": "TXT",
                "hash": "",
                "id": "0e2e7fb0-88ba-4aa4-92ef-079191b4a668",
                "last_modified": "2020-09-07T15:19:36.419018",
                "metadata_modified": None,
                "mimetype": "text/plain",
                "mimetype_inner": None,
                "name": "Dataset_2_SDM_data.txt",
                "package_id": "0f81429a-204e-4720-929e-5b251e9ab1c4",
                "position": 1,
                "resource_size": '{"size_value": "", "size_units": "kb"}',
                "resource_type": None,
                "restricted": '{"level": "same_organization", "allowed_users": "marco_moretti-wsl_ch,joan_casanelles-wsl_ch", "shared_secret": ""}',
                "size": 65679611,
                "state": "active",
                "url": "https://www.envidat.ch/dataset/0f81429a-204e-4720-929e-5b251e9ab1c4/resource/0e2e7fb0-88ba-4aa4-92ef-079191b4a668/download/dataset_2_sdm_data.txt",
                "url_type": "upload",
            },
            {
                "cache_last_updated": None,
                "cache_url": None,
                "created": "2020-09-07T15:20:43.446679",
                "description": "contains the raw data to perform the species richness models of the hypercommon species",
                "doi": "",
                "format": "TXT",
                "hash": "",
                "id": "0ef3b508-b8e7-4404-a7b9-edc51c7f2375",
                "last_modified": "2020-09-07T15:20:43.249061",
                "metadata_modified": None,
                "mimetype": "text/plain",
                "mimetype_inner": None,
                "name": "Dataset_3_Species_richness_hyper.txt",
                "package_id": "0f81429a-204e-4720-929e-5b251e9ab1c4",
                "position": 2,
                "resource_size": '{"size_value": "", "size_units": "kb"}',
                "resource_type": None,
                "restricted": '{"shared_secret": "", "allowed_users": "marco_moretti-wsl_ch,joan_casanelles-wsl_ch", "level": "same_organization"}',
                "size": 1373081,
                "state": "active",
                "url": "https://www.envidat.ch/dataset/0f81429a-204e-4720-929e-5b251e9ab1c4/resource/0ef3b508-b8e7-4404-a7b9-edc51c7f2375/download/dataset_3_species_richness_hyper.txt",
                "url_type": "upload",
            },
            {
                "cache_last_updated": None,
                "cache_url": None,
                "created": "2020-09-07T15:21:27.435458",
                "description": "contains the raw data to perform the species richness models of the rare species",
                "doi": "",
                "format": "TXT",
                "hash": "",
                "id": "3bbbc78a-92c3-4832-b51b-61d65346460e",
                "last_modified": "2020-09-07T15:21:27.252544",
                "metadata_modified": None,
                "mimetype": "text/plain",
                "mimetype_inner": None,
                "name": "Dataset_4_Species_richness_rare.txt",
                "package_id": "0f81429a-204e-4720-929e-5b251e9ab1c4",
                "position": 3,
                "resource_size": '{"size_value": "", "size_units": "kb"}',
                "resource_type": None,
                "restricted": '{"level": "same_organization", "allowed_users": "marco_moretti-wsl_ch,joan_casanelles-wsl_ch", "shared_secret": ""}',
                "size": 2274863,
                "state": "active",
                "url": "https://www.envidat.ch/dataset/0f81429a-204e-4720-929e-5b251e9ab1c4/resource/3bbbc78a-92c3-4832-b51b-61d65346460e/download/dataset_4_species_richness_rare.txt",
                "url_type": "upload",
            },
            {
                "cache_last_updated": None,
                "cache_url": None,
                "created": "2020-09-07T15:22:28.765321",
                "description": "contains the raw data to perform the species richness models of all species\r\n",
                "doi": "",
                "format": "TXT",
                "hash": "",
                "id": "f3abc8d4-c92e-4a57-aea4-39ba8c93158d",
                "last_modified": "2020-09-07T15:22:28.580170",
                "metadata_modified": None,
                "mimetype": "text/plain",
                "mimetype_inner": None,
                "name": "Dataset_5_Species_richness_all.txt",
                "package_id": "0f81429a-204e-4720-929e-5b251e9ab1c4",
                "position": 4,
                "resource_size": '{"size_value": "", "size_units": "kb"}',
                "resource_type": None,
                "restricted": '{"shared_secret": "", "allowed_users": "marco_moretti-wsl_ch,joan_casanelles-wsl_ch", "level": "same_organization"}',
                "size": 2452421,
                "state": "active",
                "url": "https://www.envidat.ch/dataset/0f81429a-204e-4720-929e-5b251e9ab1c4/resource/f3abc8d4-c92e-4a57-aea4-39ba8c93158d/download/dataset_5_species_richness_all.txt",
                "url_type": "upload",
            },
        ],
        "tags": [
            {
                "display_name": "ARTHROPODS",
                "id": "933b2f75-a0ed-4a25-a984-44b66f0c3bfd",
                "name": "ARTHROPODS",
                "state": "active",
                "vocabulary_id": None,
            },
            {
                "display_name": "BIRDS",
                "id": "0e8e27f0-fc1f-49f3-bb09-717cbccb6c32",
                "name": "BIRDS",
                "state": "active",
                "vocabulary_id": None,
            },
            {
                "display_name": "DIVERSITY",
                "id": "6333fb3f-2838-4496-88bb-3e67160e2d4d",
                "name": "DIVERSITY",
                "state": "active",
                "vocabulary_id": None,
            },
            {
                "display_name": "INSECTS",
                "id": "727d285b-f4e8-4bc7-8e71-e63ed9252bf6",
                "name": "INSECTS",
                "state": "active",
                "vocabulary_id": None,
            },
            {
                "display_name": "SDMS",
                "id": "1feba39d-6f50-4300-b5ba-6adc00490ee0",
                "name": "SDMS",
                "state": "active",
                "vocabulary_id": None,
            },
            {
                "display_name": "SNAILS",
                "id": "92a892d7-13e7-43a7-98b2-339c6cb4b3c1",
                "name": "SNAILS",
                "state": "active",
                "vocabulary_id": None,
            },
            {
                "display_name": "SPECIES ABUNDANCE DISTRIBUTIONS",
                "id": "3d02d873-d64b-4164-b73a-d0123c3e7128",
                "name": "SPECIES ABUNDANCE DISTRIBUTIONS",
                "state": "active",
                "vocabulary_id": None,
            },
            {
                "display_name": "SPECIES RICHNESS MODELS",
                "id": "e61b9a3f-fa0d-4e90-ae32-279ad9ceda29",
                "name": "SPECIES RICHNESS MODELS",
                "state": "active",
                "vocabulary_id": None,
            },
            {
                "display_name": "SPIDERS",
                "id": "3762a970-222d-4cb3-ab58-bf79e164e5ed",
                "name": "SPIDERS",
                "state": "active",
                "vocabulary_id": None,
            },
            {
                "display_name": "URBAN ECOLOGY",
                "id": "68337815-ea2a-4f12-8c28-013f9971878e",
                "name": "URBAN ECOLOGY",
                "state": "active",
                "vocabulary_id": None,
            },
            {
                "display_name": "URBANIZATION",
                "id": "80141c83-e3e9-43b5-9c76-abad1e74852c",
                "name": "URBANIZATION",
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
            "author": "[{\"name\": \"Casanelles-Abella\", \"data_credit\": [\"validation\", \"curation\", \"software\", \"publication\"], \"affiliation\": \"Conservation Biology, Biodiversity and Conservation Biology, Swiss Federal Institute for Forest, Snow and Landscape Research WSL, 8903 Birmensdorf, Switzerland\", \"affiliation_03\": \"\", \"affiliation_02\": \"Landscape Ecology, Institute of Terrestrial Ecosystems, ETH Z\\u00fcrich, 8049 Z\\u00fcrich, Switzerland\", \"identifier\": \"0000-0003-1924-9298\", \"email\": \"joan.casanelles@wsl.ch\", \"given_name\": \"Joan\"}, {\"name\": \"Chauvier\", \"data_credit\": [\"software\", \"publication\"], \"email\": \"yohann.chauvier@wsl.ch\", \"affiliation\": \"Dynamic Macroecology, Landscape Change Science, Swiss Federal Institute for Forest, Snow and Landscape Research WSL, 8903 Birmensdorf, Switzerland\", \"affiliation_03\": \"\", \"given_name\": \"Yohann\", \"identifier\": \"0000-0001-9399-3192\", \"affiliation_02\": \"\"}, {\"name\": \"Zellweger\", \"data_credit\": [\"software\", \"publication\"], \"email\": \"florian.zellweger@wsl.ch\", \"affiliation\": \"Resource Analysis, Forest Resource and Management, Swiss Federal Institute for Forest, Snow and Landscape Research WSL, 8903 Birmensdorf, Switzerland\", \"affiliation_03\": \"\", \"affiliation_02\": \"\", \"identifier\": \"0000-0003-1265-9147\", \"given_name\": \"Florian\"}, {\"name\": \"Villiger\", \"data_credit\": [\"software\", \"publication\"], \"affiliation\": \"Landscape Ecology, Institute of Terrestrial Ecosystems, ETH Z\\u00fcrich, 8049 Z\\u00fcrich, Switzerland\", \"affiliation_03\": \"\", \"given_name\": \"Petrissa\", \"identifier\": \"\", \"email\": \"villigep@student.ethz.ch\", \"affiliation_02\": \"\"}, {\"name\": \"Frey\", \"data_credit\": [\"software\", \"publication\"], \"affiliation\": \"Conservation Biology, Biodiversity and Conservation Biology, Swiss Federal Institute for Forest, Snow and Landscape Research WSL, 8903 Birmensdorf, Switzerland\", \"affiliation_03\": \"\", \"affiliation_02\": \"Spatial Evolutionary Ecology, Biodiversity and Conservation Biology, Swiss Federal Institute for Forest, Snow and Landscape Research WSL, 8903 Birmensdorf, Switzerland\", \"identifier\": \"0000-0002-4603-0438\", \"email\": \"david.frey@wsl.ch\", \"given_name\": \"David Johannes\"}, {\"name\": \"Ginzler\", \"data_credit\": [\"software\", \"publication\"], \"affiliation\": \"Remote Sensing, Landscape Change Science, Swiss Federal Institute for Forest, Snow and Landscape Research WSL, 8903 Birmensdorf, Switzerland\", \"affiliation_03\": \"\", \"affiliation_02\": \"\", \"identifier\": \"0000-0001-6365-2151\", \"email\": \"christian.ginzler@wsl.ch\", \"given_name\": \"Christian\"}, {\"name\": \"Moretti\", \"data_credit\": [\"collection\", \"publication\", \"supervision\"], \"email\": \"marco.moretti@wsl.ch\", \"affiliation\": \"Conservation Biology, Biodiversity and Conservation Biology, Swiss Federal Institute for Forest, Snow and Landscape Research WSL, 8903 Birmensdorf, Switzerland\", \"affiliation_03\": \"\", \"given_name\": \"Marco\", \"identifier\": \"0000-0002-5845-3198\", \"affiliation_02\": \"\"}, {\"name\": \"Pellissier\", \"data_credit\": [\"publication\", \"supervision\"], \"affiliation\": \"Landscape Ecology, Institute of Terrestrial Ecosystems, ETH Z\\u00fcrich, 8049 Z\\u00fcrich, Switzerland\", \"affiliation_03\": \"\", \"given_name\": \"Loic\", \"identifier\": \"0000-0002-2289-8259\", \"email\": \"loic.pellissier@wsl.ch\", \"affiliation_02\": \"Landscape Ecology, Landscape Change Science, Swiss Federal Institute for Forest, Snow and Landscape Research WSL, 8903 Birmensdorf, Switzerland\"}]",
            "author_email": null,
            "creator_user_id": "c7314170-c2ac-46d6-9193-eee220229e8b",
            "date": "[{\"date\": \"01.08.2006\", \"date_type\": \"collected\", \"end_date\": \"16.09.2007\"}, {\"date\": \"25.05.2010\", \"date_type\": \"collected\", \"end_date\": \"03.09.2010\"}, {\"date\": \"06.01.2015\", \"date_type\": \"collected\", \"end_date\": \"20.09.2016\"}, {\"date\": \"2017-02-01\", \"date_type\": \"collected\", \"end_date\": \"2017-10-31\"}]",
            "doi": "10.16904/envidat.172",
            "funding": "[{\"grant_number\": \"H2020, BiodivERsA32015104\", \"institution\": \"Swiss National Science Foundation (project 31BD30_172467) within the programme ERA-Net BiodivERsA project \u201cBioVEINS: Connectivity of green and blue infrastructures: living veins for biodiverse and healthy cities\u201d (H2020 BiodivERsA32015104)\", \"institution_url\": \"http://bioveins.eu, https://www.biodiversa.org, http://p3.snf.ch/project-172467\"}, {\"grant_number\": \"172198\", \"institution\": \"F.Z. received funding from the Swiss National Science Foundation (project 172198)\", \"institution_url\": \"http://p3.snf.ch/project-172198\"}, {\"grant_number\": \"310030L_170059\", \"institution\": \"Y.C. acknowledges the ANR-SNF bilateral project OriginAlps (grant number 310030L_170059)\", \"institution_url\": \"http://p3.snf.ch/project-170059\"}]",
            "id": "0f81429a-204e-4720-929e-5b251e9ab1c4",
            "isopen": false,
            "language": "en",
            "license_id": "other-undefined",
            "license_title": "Other (Specified in the description)",
            "maintainer": "{\"affiliation\": \"Conservation Biology, Biodiversity and Conservation Biology, Swiss Federal Institute for Forest, Snow and Landscape Research WSL, 8903 Birmensdorf, Switzerland\", \"email\": \"marco.moretti@wsl.ch\", \"name\": \"Moretti\", \"identifier\": \"0000-0002-5845-3198\", \"given_name\": \"Marco\"}",
            "maintainer_email": null,
            "metadata_created": "2020-09-07T15:14:02.051289",
            "metadata_modified": "2020-09-17T09:14:48.641088",
            "name": "ecological-properties-of-urban-ecosystems-biodiversity-dataset-of-zurich",
            "notes": "Richness, site occurrence and abundance data of bees, beetles, birds, hoverflies, net-wingeds, true bugs, snails, spiders, milipides, wasps collected in the city of Zurich using different sampling techniques, and the environmental variables for each sampling site.\r\nData are provided on request to contact person against bilateral agreement.",
            "num_resources": 5,
            "num_tags": 11,
            "organization": {
                "id": "32672ec5-c180-471e-92f7-ef58e00eb1fb",
                "name": "conservation-biology",
                "title": "Conservation Biology",
                "type": "organization",
                "description": "We study the relationship between threatened species and their habitat with the objective to develop evidence-based instruments for conservation. The viability of populations of habitat specialists is often limited due to restricted availability of suitable habitat or discontinuous distribution. We focus on selected animal species of conservation concern (forest birds, bats, forest insects) and analyse species-habitat relationships at a scale ranging from single subpopulations to entire metapopulations. We strive towards standardised recording of elusive species with novel techniques, assessing environmental variables and combining these field data with data from remote sensing. We determine limiting factors (habitat, climate, resources) and predict species occurrence and habitat suitability with modelling techniques.\r\n\r\nThese models allow to predict species occurrence patterns and to delineate evidence-based priority areas for conservation. Our long-term collaboration with federal and cantonal stakeholders of forest and nature conservation enables the combination of research results with conservation requirements (e.g. species action plans, forest biodiversity expert panel, scientific counsel for bat protection). While we investigate complete distribution ranges in bats, we focus on forest habitats in birds and insects given the large extent and high importance of forests for biodiversity conservation in Switzerland.",
                "image_url": "2018-07-10-090115.162284LogoWSL.svg",
                "created": "2018-05-18T09:12:30.577470",
                "is_organization": true,
                "approval_status": "approved",
                "state": "active"
            },
            "owner_org": "32672ec5-c180-471e-92f7-ef58e00eb1fb",
            "private": false,
            "publication": "{\"publisher\": \"EnviDat\", \"publication_year\": \"2020\"}",
            "publication_state": "published",
            "related_datasets": "* Dataset_1_SAD_SOD.txt\r\n* Dataset_2_SDM_data.txt\r\n* Dataset_3_Species_richness_hyper.txt\r\n* Dataset_4_Species_richness_rare.txt\r\n* Dataset_5_Species_richness_all.txt\r\n*\r\nData extracts in TAB-delimted format. First row is header",
            "related_publications": "",
            "resource_type": "dataset",
            "resource_type_general": "dataset",
            "spatial": "{\"type\":\"Polygon\",\"coordinates\":[[[8.463935852050781,47.329748306633896],[8.463935852050781,47.427622733649606],[8.602638244628906,47.427622733649606],[8.602638244628906,47.329748306633896],[8.463935852050781,47.329748306633896]]]}",
            "spatial_info": "Switzerland",
            "state": "active",
            "subtitle": "",
            "title": "Ecological properties of urban ecosystems. Biodiversity dataset of Zurich",
            "type": "dataset",
            "url": null,
            "version": "1.0",
            "resources": [
                {
                    "cache_last_updated": null,
                    "cache_url": null,
                    "created": "2020-09-07T15:18:31.256479",
                    "description": "abundance and occurrence data of the 1446 species studied, used to investigate species-abundance distributions and species-occurrence distributions",
                    "doi": "",
                    "format": "TXT",
                    "hash": "",
                    "id": "a7a96a85-dc46-4b5f-bcf4-4d91485e3d03",
                    "last_modified": "2020-09-07T15:18:31.071900",
                    "metadata_modified": null,
                    "mimetype": "text/plain",
                    "mimetype_inner": null,
                    "name": "Dataset_1_SAD_SOD.txt",
                    "package_id": "0f81429a-204e-4720-929e-5b251e9ab1c4",
                    "position": 0,
                    "resource_size": "{\"size_value\": \"\", \"size_units\": \"kb\"}",
                    "resource_type": null,
                    "restricted": "{\"shared_secret\": \"\", \"allowed_users\": \"marco_moretti-wsl_ch,joan_casanelles-wsl_ch\", \"level\": \"same_organization\"}",
                    "size": 73478,
                    "state": "active",
                    "url": "https://www.envidat.ch/dataset/0f81429a-204e-4720-929e-5b251e9ab1c4/resource/a7a96a85-dc46-4b5f-bcf4-4d91485e3d03/download/dataset_1_sad_sod.txt",
                    "url_type": "upload"
                },
                {
                    "cache_last_updated": null,
                    "cache_url": null,
                    "created": "2020-09-07T15:19:36.603618",
                    "description": "contains the raw data to perform species distribution models, only for common species",
                    "doi": "",
                    "format": "TXT",
                    "hash": "",
                    "id": "0e2e7fb0-88ba-4aa4-92ef-079191b4a668",
                    "last_modified": "2020-09-07T15:19:36.419018",
                    "metadata_modified": null,
                    "mimetype": "text/plain",
                    "mimetype_inner": null,
                    "name": "Dataset_2_SDM_data.txt",
                    "package_id": "0f81429a-204e-4720-929e-5b251e9ab1c4",
                    "position": 1,
                    "resource_size": "{\"size_value\": \"\", \"size_units\": \"kb\"}",
                    "resource_type": null,
                    "restricted": "{\"level\": \"same_organization\", \"allowed_users\": \"marco_moretti-wsl_ch,joan_casanelles-wsl_ch\", \"shared_secret\": \"\"}",
                    "size": 65679611,
                    "state": "active",
                    "url": "https://www.envidat.ch/dataset/0f81429a-204e-4720-929e-5b251e9ab1c4/resource/0e2e7fb0-88ba-4aa4-92ef-079191b4a668/download/dataset_2_sdm_data.txt",
                    "url_type": "upload"
                },
                {
                    "cache_last_updated": null,
                    "cache_url": null,
                    "created": "2020-09-07T15:20:43.446679",
                    "description": "contains the raw data to perform the species richness models of the hypercommon species",
                    "doi": "",
                    "format": "TXT",
                    "hash": "",
                    "id": "0ef3b508-b8e7-4404-a7b9-edc51c7f2375",
                    "last_modified": "2020-09-07T15:20:43.249061",
                    "metadata_modified": null,
                    "mimetype": "text/plain",
                    "mimetype_inner": null,
                    "name": "Dataset_3_Species_richness_hyper.txt",
                    "package_id": "0f81429a-204e-4720-929e-5b251e9ab1c4",
                    "position": 2,
                    "resource_size": "{\"size_value\": \"\", \"size_units\": \"kb\"}",
                    "resource_type": null,
                    "restricted": "{\"shared_secret\": \"\", \"allowed_users\": \"marco_moretti-wsl_ch,joan_casanelles-wsl_ch\", \"level\": \"same_organization\"}",
                    "size": 1373081,
                    "state": "active",
                    "url": "https://www.envidat.ch/dataset/0f81429a-204e-4720-929e-5b251e9ab1c4/resource/0ef3b508-b8e7-4404-a7b9-edc51c7f2375/download/dataset_3_species_richness_hyper.txt",
                    "url_type": "upload"
                },
                {
                    "cache_last_updated": null,
                    "cache_url": null,
                    "created": "2020-09-07T15:21:27.435458",
                    "description": "contains the raw data to perform the species richness models of the rare species",
                    "doi": "",
                    "format": "TXT",
                    "hash": "",
                    "id": "3bbbc78a-92c3-4832-b51b-61d65346460e",
                    "last_modified": "2020-09-07T15:21:27.252544",
                    "metadata_modified": null,
                    "mimetype": "text/plain",
                    "mimetype_inner": null,
                    "name": "Dataset_4_Species_richness_rare.txt",
                    "package_id": "0f81429a-204e-4720-929e-5b251e9ab1c4",
                    "position": 3,
                    "resource_size": "{\"size_value\": \"\", \"size_units\": \"kb\"}",
                    "resource_type": null,
                    "restricted": "{\"level\": \"same_organization\", \"allowed_users\": \"marco_moretti-wsl_ch,joan_casanelles-wsl_ch\", \"shared_secret\": \"\"}",
                    "size": 2274863,
                    "state": "active",
                    "url": "https://www.envidat.ch/dataset/0f81429a-204e-4720-929e-5b251e9ab1c4/resource/3bbbc78a-92c3-4832-b51b-61d65346460e/download/dataset_4_species_richness_rare.txt",
                    "url_type": "upload"
                },
                {
                    "cache_last_updated": null,
                    "cache_url": null,
                    "created": "2020-09-07T15:22:28.765321",
                    "description": "contains the raw data to perform the species richness models of all species\r\n",
                    "doi": "",
                    "format": "TXT",
                    "hash": "",
                    "id": "f3abc8d4-c92e-4a57-aea4-39ba8c93158d",
                    "last_modified": "2020-09-07T15:22:28.580170",
                    "metadata_modified": null,
                    "mimetype": "text/plain",
                    "mimetype_inner": null,
                    "name": "Dataset_5_Species_richness_all.txt",
                    "package_id": "0f81429a-204e-4720-929e-5b251e9ab1c4",
                    "position": 4,
                    "resource_size": "{\"size_value\": \"\", \"size_units\": \"kb\"}",
                    "resource_type": null,
                    "restricted": "{\"shared_secret\": \"\", \"allowed_users\": \"marco_moretti-wsl_ch,joan_casanelles-wsl_ch\", \"level\": \"same_organization\"}",
                    "size": 2452421,
                    "state": "active",
                    "url": "https://www.envidat.ch/dataset/0f81429a-204e-4720-929e-5b251e9ab1c4/resource/f3abc8d4-c92e-4a57-aea4-39ba8c93158d/download/dataset_5_species_richness_all.txt",
                    "url_type": "upload"
                }
            ],
            "tags": [
                {
                    "display_name": "ARTHROPODS",
                    "id": "933b2f75-a0ed-4a25-a984-44b66f0c3bfd",
                    "name": "ARTHROPODS",
                    "state": "active",
                    "vocabulary_id": null
                },
                {
                    "display_name": "BIRDS",
                    "id": "0e8e27f0-fc1f-49f3-bb09-717cbccb6c32",
                    "name": "BIRDS",
                    "state": "active",
                    "vocabulary_id": null
                },
                {
                    "display_name": "DIVERSITY",
                    "id": "6333fb3f-2838-4496-88bb-3e67160e2d4d",
                    "name": "DIVERSITY",
                    "state": "active",
                    "vocabulary_id": null
                },
                {
                    "display_name": "INSECTS",
                    "id": "727d285b-f4e8-4bc7-8e71-e63ed9252bf6",
                    "name": "INSECTS",
                    "state": "active",
                    "vocabulary_id": null
                },
                {
                    "display_name": "SDMS",
                    "id": "1feba39d-6f50-4300-b5ba-6adc00490ee0",
                    "name": "SDMS",
                    "state": "active",
                    "vocabulary_id": null
                },
                {
                    "display_name": "SNAILS",
                    "id": "92a892d7-13e7-43a7-98b2-339c6cb4b3c1",
                    "name": "SNAILS",
                    "state": "active",
                    "vocabulary_id": null
                },
                {
                    "display_name": "SPECIES ABUNDANCE DISTRIBUTIONS",
                    "id": "3d02d873-d64b-4164-b73a-d0123c3e7128",
                    "name": "SPECIES ABUNDANCE DISTRIBUTIONS",
                    "state": "active",
                    "vocabulary_id": null
                },
                {
                    "display_name": "SPECIES RICHNESS MODELS",
                    "id": "e61b9a3f-fa0d-4e90-ae32-279ad9ceda29",
                    "name": "SPECIES RICHNESS MODELS",
                    "state": "active",
                    "vocabulary_id": null
                },
                {
                    "display_name": "SPIDERS",
                    "id": "3762a970-222d-4cb3-ab58-bf79e164e5ed",
                    "name": "SPIDERS",
                    "state": "active",
                    "vocabulary_id": null
                },
                {
                    "display_name": "URBAN ECOLOGY",
                    "id": "68337815-ea2a-4f12-8c28-013f9971878e",
                    "name": "URBAN ECOLOGY",
                    "state": "active",
                    "vocabulary_id": null
                },
                {
                    "display_name": "URBANIZATION",
                    "id": "80141c83-e3e9-43b5-9c76-abad1e74852c",
                    "name": "URBANIZATION",
                    "state": "active",
                    "vocabulary_id": null
                }
            ],
            "groups": [],
            "relationships_as_subject": [],
            "relationships_as_object": []
        }"""
    ).strip()

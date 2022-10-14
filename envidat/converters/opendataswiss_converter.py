import logging
import json

from typing import Optional
from collections import OrderedDict
from dateutil.parser import parse
from xmltodict import unparse

from envidat.api.v1 import get_metadata_list_with_resources


log = logging.getLogger(__name__)


def convert_opendataswiss() -> str:
    """Generate XML formatted string in OpenDataSwiss format for ALL packages combined
    into one XML string.

    Note:
        Converter is only valid for the metadata schema for EnviDat.

    Returns:
        str: XML formatted string in OpenDataSwiss format for all packages combined.
        (see https://www.envidat.ch/opendata/export/dcat-ap-ch.xml)
    """

    converted_packages = []
    metadata_list = get_metadata_list_with_resources()

    # Try to convert packages to OrderedDictionaries compatible with OpenDataSwiss
    # format, then convert dictionaries to XML
    try:
        for package in metadata_list:
            # Convert each package (metadata record) in package_list to XML format
            package_dict = opendataswiss_convert_dataset(package)
            if package_dict:
                converted_packages += [package_dict]
            else:
                log.error(f"ERROR: Failed to convert {package}")

        # Wrap converted_packages into wrapper dictionary with catalog and root tags
        wrapper_dict = get_wrapper_dict(converted_packages)

        # Convert wrapper_dict to XML format
        converted_data_xml = unparse(wrapper_dict, short_empty_elements=True,
                                     pretty=True)

        return converted_data_xml

    except ValueError as e:
        log.error(e)
        log.error("Cannot convert packages to OpenDataSwiss format.")
        raise ValueError("Failed to convert packages to OpenDataSwiss format.")


def opendataswiss_convert_dataset(package: dict) -> Optional[OrderedDict]:
    """Return OpenDataSwiss formatted OrderedDict from EnviDat JSON."""

    try:

        md_metadata_dict = OrderedDict()

        # Dataset URL
        package_name = package["name"]
        package_url = f"https://www.envidat.ch/#/metadata/{package_name}"
        md_metadata_dict["dcat:Dataset"] = {"@rdf:about": package_url}

        # identifier
        package_id = package["id"]
        md_metadata_dict["dcat:Dataset"]["dct:identifier"] = f"{package_id}@envidat"

        # title
        title = package["title"]
        md_metadata_dict["dcat:Dataset"]["dct:title"] = {
            "@xml:lang": "en",
            "#text": title,
        }

        # description
        description = clean_text(package.get("notes", ""))
        md_metadata_dict["dcat:Dataset"]["dct:description"] = {
            "@xml:lang": "en",
            "#text": description,
        }

        # issued
        creation_date = package.get("metadata_created")
        if creation_date:
            md_metadata_dict["dcat:Dataset"]["dct:issued"] = {
                "@rdf:datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                "#text": parse(creation_date).strftime("%Y-%m-%dT%H:%M:%SZ"),
            }

        # modified
        modification_date = package.get("metadata_modified", creation_date)
        if modification_date:
            md_metadata_dict["dcat:Dataset"]["dct:modified"] = {
                "@rdf:datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                "#text": parse(modification_date).strftime("%Y-%m-%dT%H:%M:%SZ"),
            }

        # publication (MANDATORY)
        md_metadata_dict["dcat:Dataset"]["dct:publisher"] = {
            "foaf:Organization": {
                "@rdf:about": "https://envidat.ch/#/about",
                "foaf:name": "EnviDat",
            }
        }

        # landing page
        md_metadata_dict["dcat:Dataset"]["dcat:landingPage"] = {
            "@rdf:resource": package_url
        }

        # contact point (MANDATORY)
        maintainer = json.loads(package.get("maintainer", "{}"))
        maintainer_name = ""

        if maintainer.get("given_name"):
            maintainer_name += maintainer["given_name"].strip() + " "

        maintainer_name += maintainer["name"]
        maintainer_email = "mailto:" + maintainer["email"]
        individual_contact_point = {
            "vcard:Individual": {
                "vcard:fn": maintainer_name,
                "vcard:hasEmail": {"@rdf:resource": maintainer_email},
            }
        }

        if maintainer_email == "mailto:envidat@wsl.ch":
            md_metadata_dict["dcat:Dataset"]["dcat:contactPoint"] = [
                individual_contact_point
            ]
        else:
            organization_contact_point = {
                "vcard:Organization": {
                    "vcard:fn": "EnviDat Support",
                    "vcard:hasEmail": {"@rdf:resource": "mailto:envidat@wsl.ch"},
                }
            }
            md_metadata_dict["dcat:Dataset"]["dcat:contactPoint"] = [
                individual_contact_point,
                organization_contact_point,
            ]

        # theme (MANDATORY)
        md_metadata_dict["dcat:Dataset"]["dcat:theme"] = {
            "@rdf:resource": "http://opendata.swiss/themes/education"
        }

        # language
        md_metadata_dict["dcat:Dataset"]["dct:language"] = {"#text": "en"}

        # keyword
        keywords_list = []
        keywords = get_keywords(package)
        for keyword in keywords:
            keywords_list += [{"@xml:lang": "en", "#text": keyword}]
        md_metadata_dict["dcat:Dataset"]["dcat:keyword"] = keywords_list

        # Distribution - iterate through package resources and obtain
        # package license (MANDATORY)
        # Call get_distribution_list(package) to get distibution list
        md_metadata_dict["dcat:Dataset"]["dcat:distribution"] = get_distribution_list(
            package, package_name
        )

        return md_metadata_dict

    except Exception as e:
        log.error(f"ERROR: Cannot convert {package} to OpenDataSwiss format.")
        log.error(e)
        return None


def clean_text(text: str) -> str:
    """Returns text cleaned of hashes and with modified characters"""

    cleaned_text = (
        text.replace("###", "")
        .replace("##", "")
        .replace(" #", " ")
        .replace("# ", " ")
        .replace("__", "")
        .replace("  ", " ")
        .replace("\r", "\n")
        .replace("\n\n", "\n")
    )
    return cleaned_text


def get_keywords(package: dict) -> list:
    """Returns keywords from tags in package (metadata record)."""

    keywords = []
    for tag in package.get("tags", []):
        name = tag.get("display_name", "").upper()
        keywords += [name]
    return keywords


def get_distribution_list(package: dict, package_name: str) -> list:
    """Return distribution_list created from package resources list and licence_id."""

    distribution_list = []

    dataset_license = package.get("license_id", "odc-odbl")

    license_mapping = {
        "wsl-data": (
            "NonCommercialWithPermission-CommercialWithPermission-ReferenceRequired"
        ),
        "odc-odbl": "NonCommercialAllowed-CommercialAllowed-ReferenceRequired",
        "cc-by": "NonCommercialAllowed-CommercialAllowed-ReferenceRequired",
        "cc-by-sa": "NonCommercialAllowed-CommercialAllowed-ReferenceRequired",
        "cc-zero": "NonCommercialAllowed-CommercialAllowed-ReferenceNotRequired",
        "CC0-1.0": "NonCommercialAllowed-CommercialAllowed-ReferenceNotRequired",
    }
    resource_license = license_mapping.get(
        dataset_license,
        "NonCommercialWithPermission-CommercialWithPermission-ReferenceRequired",
    )

    for resource in package.get("resources", []):

        resource_id = resource.get("id")
        resource_name = resource.get("name", resource_id)
        resource_notes = clean_text(resource.get("description", "No description"))
        resource_page_url = (
            f"https://www.envidat.ch/dataset/{package_name}/resource/"
            + resource.get("id", "")
        )
        resource_url = resource.get("url")

        resource_creation = parse(resource["created"]).strftime("%Y-%m-%dT%H:%M:%SZ")
        resource_modification = resource_creation
        if resource.get("last_modified", resource.get("metadata_modified", "")):
            resource_modification = parse(
                resource.get("last_modified", resource.get("metadata_modified", ""))
            ).strftime("%Y-%m-%dT%H:%M:%SZ")

        resource_size = resource.get("size", False)

        if not resource_size:
            resource_size = 0
            try:
                if len(resource.get("resource_size", "")) > 0:
                    resource_size_obj = json.loads(
                        resource.get("resource_size", "{'size_value': '0'}")
                    )
                    sizes_dict = {
                        "KB": 1024,
                        "MB": 1048576,
                        "GB": 1073741824,
                        "TB": 1099511627776,
                    }
                    resource_size_str = resource_size_obj.get("size_value", "")
                    if len(resource_size_str) > 0:
                        resource_size = (
                            float(resource_size_obj.get("size_value", "0"))
                            * sizes_dict[
                                resource_size_obj.get("size_units", "KB").upper()
                            ]
                        )
            except Exception as e:
                log.error(
                    "resource {} unparseable resource_size: {}".format(
                        resource_url, resource.get("resource_size")
                    )
                )
                log.error(e)
                resource_size = 0

        resource_mimetype = resource.get("mimetype", "")
        if not resource_mimetype or len(resource_mimetype) == 0:
            resource_mimetype = resource.get("mimetype_inner")

        resource_format = resource.get("format")

        distribution = {
            "dcat:Distribution": {
                "@rdf:about": resource_page_url,
                "dct:identifier": package["name"] + "." + resource_id,
                "dct:title": {"@xml:lang": "en", "#text": resource_name},
                "dct:description": {"@xml:lang": "en", "#text": resource_notes},
                "dct:issued": {
                    "@rdf:datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "#text": resource_creation,
                },
                "dct:modified": {
                    "@rdf:datatype": "http://www.w3.org/2001/XMLSchema#dateTime",
                    "#text": resource_modification,
                },
                "dct:language": "en",
                "dcat:accessURL": {
                    "@rdf:resource": resource_page_url,
                },
                "dct:rights": resource_license,
                "dcat:byteSize": resource_size,
            }
        }
        # mediaType
        if resource_mimetype:
            distribution["dcat:Distribution"]["dcat:mediaType"] = resource_mimetype

        # format
        if resource_format:
            distribution["dcat:Distribution"]["dct:format"] = resource_format

        distribution_list += [distribution]

    return distribution_list


def get_wrapper_dict(converted_packages: list) -> dict:
    """
    Returns wrapper dictionary (with catalog and root tags)
    for converted packages.
    """

    # Assign catalog_dict for header and converted_packages
    catalog_dict = OrderedDict()

    # header
    catalog_dict["@xmlns:dct"] = "http://purl.org/dc/terms/"
    catalog_dict["@xmlns:dc"] = "http://purl.org/dc/elements/1.1/"
    catalog_dict["@xmlns:dcat"] = "http://www.w3.org/ns/dcat#"
    catalog_dict["@xmlns:foaf"] = "http://xmlns.com/foaf/0.1/"
    catalog_dict["@xmlns:xsd"] = "http://www.w3.org/2001/XMLSchema#"
    catalog_dict["@xmlns:rdfs"] = "http://www.w3.org/2000/01/rdf-schema#"
    catalog_dict["@xmlns:rdf"] = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    catalog_dict["@xmlns:vcard"] = "http://www.w3.org/2006/vcard/ns#"
    catalog_dict["@xmlns:odrs"] = "http://schema.theodi.org/odrs#"
    catalog_dict["@xmlns:schema"] = "http://schema.org/"

    catalog_dict["dcat:Catalog"] = {"dcat:dataset": converted_packages}

    # Assign dcat_catalog_dict dictionary for root element in XML file
    dcat_catalog_dict = OrderedDict()
    dcat_catalog_dict["rdf:RDF"] = catalog_dict

    return dcat_catalog_dict

"""DataCite for linking metadata to DOIs."""

import collections
import json
import os
import re
from json import JSONDecodeError
from logging import getLogger

import validators
from xmltodict import unparse

from envidat.utils import get_url

log = getLogger(__name__)


# TODO investigate if name_doi_map needed
def convert_datacite(metadata_record: dict, name_doi_map: dict) -> str:
    """Generate XML formatted string in DataCite format.

    Note:
        Converter is only valid for the metadata schema for EnviDat.

    Args:
        metadata_record (dict): Individual EnviDat metadata entry record dictionary.
        name_doi_map (dict): Mapping of dataset name to DOI, as dictionary name:doi.

    Returns:
        str: XML formatted string compatible with DataCite DIF 10.2 standard
    """
    try:
        # TODO finish refactoring Datacite converter
        # config: dict = get_config_datacite_converter()
        # converted_package = datacite_convert_dataset_test(metadata_record, config)

        converted_package = datacite_convert_dataset(metadata_record, name_doi_map)
        return unparse(converted_package, pretty=True)  # Convert OrderedDict to XML
    except ValueError as e:
        log.error(e)
        log.error("Cannot convert package to DataCite format.")
        raise ValueError("Failed to convert package to DataCite format.")


# TODO possibly implement JSON schema to make sure all required keys included in config,
#  see https://pypi.org/project/jsonschema/ and
#  https://towardsdatascience.com/how-to-use-json-schema-to-validate-json-documents-ae9d8d1db344
def get_config_datacite_converter() -> dict:
    """Return datacite converter JSON config as Python dictionary.
    Dictionary maps Datacite XML schema tags (keys)
    to EnviDat schema fields (values).
    """
    with open("envidat/converters/config_converters.json") as config_json:
        config: dict = json.load(config_json)
        datacite_config: dict = config["datacite_converter"]
    return datacite_config


# TODO connect DataCite converter to DOI CKAN extension
# TODO test refactoring datacite_covert_datasets() using dictionary of Datacite schema
#  keys and corresponding EnviDat schema fields as values
# TODO remove longer blocks to separate helper functions
# TODO keep in mind that a reverse converter will
#  also need to be written (Datacite to EnviDat)
# TODO investigate if any additional fields from EnviDat schema can be matched
#  to Datacite schema, for example custom fields
# TODO investigate if name_doi_map needed
# TODO write docstring
def datacite_convert_dataset_test(dataset: dict, config: dict):
    """Convert EnviDat metadata package from CKAN to DataCite XML."""

    # Assign datacite to ordered dictionary that will contain
    # dataset content converted to DataCite format
    datacite = collections.OrderedDict()

    # Assign language tag used several times in function
    datacite_xml_lang_tag = "xml:lang"

    # Header
    datacite["resource"] = collections.OrderedDict()
    namespace = "http://datacite.org/schema/kernel-4"
    schema = "http://schema.datacite.org/meta/kernel-4.4/metadata.xsd"
    datacite["resource"]["@xsi:schemaLocation"] = f"{namespace} {schema}"
    datacite["resource"]["@xmlns"] = f"{namespace}"
    datacite["resource"]["@xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"

    # Identifier
    datacite_identifier_tag = "identifier"
    doi = dataset.get(config[datacite_identifier_tag], "")
    datacite["resource"][datacite_identifier_tag] = {
        "#text": doi.strip(),
        "@identifierType": "DOI",
    }

    # Creators
    datacite_creators_tag = "creators"
    datacite_creator_tag = "creator"
    datacite["resource"][datacite_creators_tag] = {datacite_creator_tag: []}
    author_dataset = dataset.get(config[datacite_creators_tag], [])
    try:
        authors = json.loads(author_dataset)
    except JSONDecodeError:
        authors = []

    for author in authors:
        datacite_creator = get_datacite_creator(author, config)
        datacite["resource"][datacite_creators_tag][datacite_creator_tag] += [
            datacite_creator
        ]

    # Titles
    datacite_titles_tag = "titles"
    datacite_title_tag = "title"
    datacite["resource"][datacite_titles_tag] = {datacite_title_tag: []}
    title = dataset.get(config[datacite_title_tag], "")
    if title:
        datacite["resource"][datacite_titles_tag][datacite_title_tag] = {
            f"@{datacite_xml_lang_tag}": "en-us",
            "#text": title,
        }

    # Get publication dictionary
    pub = dataset.get("publication", {})
    try:
        publication = json.loads(pub)
    except JSONDecodeError:
        publication = {}

    # Publication year
    datacite_publication_year_tag = "publicationYear"
    publication_year = publication.get(config[datacite_publication_year_tag], "")
    if publication_year:
        datacite["resource"][datacite_publication_year_tag] = {
            "#text": publication_year
        }

    # Publisher
    datacite_publisher_tag = "publisher"
    publisher = publication.get(config[datacite_publisher_tag], "")
    if publisher:
        datacite["resource"][datacite_publisher_tag] = {
            f"@{datacite_xml_lang_tag}": "en-us",
            "#text": publisher.strip(),
        }

    # Subjects
    datacite_subjects_tag = "subjects"
    datacite_subject_tag = "subject"
    datacite_subjects = []

    # Get tags list
    tags = dataset.get(config[datacite_subjects_tag], [])

    for tag in tags:
        tag_name = tag.get(config[datacite_subject_tag], tag.get("name", ""))
        datacite_subjects += [{f"@{datacite_xml_lang_tag}": "en-us", "#text": tag_name}]

    if datacite_subjects:
        datacite["resource"][datacite_subjects_tag] = {
            datacite_subject_tag: datacite_subjects
        }

    # Contributor (contact person)
    datacite_contributors_tag = "contributors"
    datacite_contributor_tag = "contributor"

    maintainer_dataset = dataset.get(config[datacite_contributors_tag], {})
    try:
        maintainer = json.loads(maintainer_dataset)
    except JSONDecodeError:
        maintainer = {}

    datacite_contributor = get_datacite_contributor(maintainer, config)

    if datacite_contributor:
        datacite["resource"][datacite_contributors_tag] = {
            datacite_contributor_tag: datacite_contributor
        }

    # Dates
    datacite_dates_tag = "dates"
    datacite_date_tag = "date"
    datacite_date_type_tag = "dateType"
    datacite_dates = []

    date_input = dataset.get(config[datacite_dates_tag], [])
    try:
        dates = json.loads(date_input)
    except JSONDecodeError:
        dates = []

    for date in dates:
        datacite_date = {
            "#text": date.get(config[datacite_date_tag], ""),
            f"@{datacite_date_type_tag}": (
                date.get(config[datacite_date_type_tag], "Valid")
            ).title(),
        }
        datacite_dates += [datacite_date]

    if datacite_dates:
        datacite["resource"][datacite_dates_tag] = {datacite_date_tag: datacite_dates}

    # TODO check if all datasets should be assigned a default language of "en"
    # Language
    datacite_language_tag = "language"
    datacite_language = dataset.get(config[datacite_language_tag], "")
    if not datacite_language:
        datacite_language = "en"
    datacite["resource"][datacite_language_tag] = {"#text": datacite_language}

    # TODO start refactoring from here!!!
    # # ResourceType
    # datacite_resource_type_tag = "resourceType"
    # datacite_resource_type_general_tag = "resourceTypeGeneral"
    # resource_type_general = dataset.get("resource_type_general", "Dataset")
    # datacite_resource_type_general = value_to_datacite_cv(
    #     resource_type_general, datacite_resource_type_general_tag, default="Dataset"
    # )
    #
    # datacite["resource"][datacite_resource_type_tag] = {
    #     "#text": dataset.get("resource_type", ""),
    #     # f'@{datacite_resource_type_general_tag}': (
    #     #     dataset.get('resource_type_general', 'Dataset'
    #     # )).title()
    #     f"@{datacite_resource_type_general_tag}": datacite_resource_type_general,
    # }
    #
    # # Alternate Identifier
    # base_url = "https://www.envidat.ch/dataset/"
    # alternate_identifiers = []
    #
    # package_name = dataset.get("name", "")
    # if package_name:
    #     package_url = f"{base_url}{package_name}"
    #     alternate_identifiers.append(
    #         {"#text": package_url, "@alternateIdentifierType": "URL"}
    #     )
    #
    # package_id = dataset.get("id", "")
    # if package_id:
    #     package_id = f"{base_url}{package_id}"
    #     alternate_identifiers.append(
    #         {"#text": package_id, "@alternateIdentifierType": "URL"}
    #     )
    #
    # datacite["resource"]["alternateIdentifiers"] = {
    #     "alternateIdentifier": alternate_identifiers
    # }
    #
    # TODO extract related identifier block to separate function
    # # Related identifier
    # datacite_related_urls = collections.OrderedDict()
    # datacite_related_urls["relatedIdentifier"] = []
    #
    # # Combine "related_publications" and "related_datasets" values
    # related_publications = dataset.get("related_publications", "")
    # related_datasets = dataset.get("related_datasets", "")
    # related_identifiers = f"${related_publications} {related_datasets}"
    #
    # # Validate related_identifiers
    # if len(related_identifiers) > 0:
    #     # Remove special characters "\r", "\n" and
    #     # remove Markdown link syntax using brackets and parentheses
    #     # and replace with one space " "
    #     related_identifiers = re.sub(r"\r|\n|\[|\]|\(|\)", " ", related_identifiers)
    #
    #     # Assign empty array to hold "related_ids" values that will be used to check for
    #     # duplicates
    #     related_ids = []
    #
    #     for word in related_identifiers.split(" "):
    #
    #         # Apply search function to find DOIs
    #         doi = get_doi(word)
    #
    #         # Apply search criteria to find DOIs from DORA API
    #         # DORA API documentation:
    #         # https://www.wiki.lib4ri.ch/display/HEL/Technical+details+of+DORA
    #         dora_str = "dora.lib4ri.ch/wsl/islandora/object/"
    #         if dora_str in word:
    #             dora_index = word.find(dora_str)
    #             dora_pid = word[(dora_index + len(dora_str)) :]
    #
    #             # Call DORA API and get DOI if it listed in citation
    #             doi_dora = get_dora_doi(dora_pid)
    #             if doi_dora:
    #                 doi = doi_dora
    #
    #         if doi and "/" in doi and doi not in related_ids:
    #             related_ids.append(doi)
    #             datacite_related_urls["relatedIdentifier"] += [
    #                 {
    #                     "#text": doi,
    #                     "@relatedIdentifierType": "DOI",
    #                     "@relationType": "isSupplementTo",
    #                 }
    #             ]
    #             continue
    #

    # TODO fix indentation here
    # # Apply URL validator to find other URLs (that are not DOIs)
    # is_url = validators.url(word)
    #
    # if all([is_url, word not in related_ids, "doi" not in word]):
    #     related_ids.append(word)
    #
    #     # EnviDat datasets are assigned a relationType of "Cites"
    #     if word.startswith(('https://envidat.ch/#/metadata/',
    #                         'https://envidat.ch/dataset/')):
    #         datacite_related_urls["relatedIdentifier"] += [
    #             {
    #                 "#text": word,
    #                 "@relatedIdentifierType": "URL",
    #                 "@relationType": "Cites",
    #             }
    #         ]
    #     else:
    #         # All other URLs are assigned a relationType of "isSupplementTo"
    #         datacite_related_urls["relatedIdentifier"] += [
    #             {
    #                 "#text": word,
    #                 "@relatedIdentifierType": "URL",
    #                 "@relationType": "isSupplementTo",
    #             }
    #         ]
    #
    # if len(datacite_related_urls["relatedIdentifier"]) > 0:
    #     datacite["resource"]["relatedIdentifiers"] = datacite_related_urls
    #
    # TODO extract sizes block to seprate block
    # # Sizes (from resources)
    # datacite_size_group_tag = "sizes"
    # datacite_size_tag = "size"
    # datacite_sizes = []
    #
    # for resource in dataset.get("resources", []):
    #     if resource.get("size", ""):
    #         datacite_sizes += [{"#text": str(resource.get("size", " ")) + " bytes"}]
    #     elif resource.get("resource_size", ""):
    #         resource_size = resource.get("resource_size", "")
    #         try:
    #             resource_size_obj = json.loads(resource_size)
    #             datacite_sizes += [
    #                 {
    #                     "#text": (
    #                         resource_size_obj.get("size_value", "0")
    #                         + " "
    #                         + resource_size_obj.get("size_unit", "KB").upper()
    #                     ).strip()
    #                 }
    #             ]
    #         except JSONDecodeError:
    #             log.error("non-parsable value at resource_size:" + str(resource_size))
    #
    # if datacite_sizes:
    #     datacite["resource"][datacite_size_group_tag] = {
    #         datacite_size_tag: datacite_sizes
    #     }
    #
    # TODO extract formats block to separate functionality
    # # Formats (from resources)
    # datacite_format_group_tag = "formats"
    # datacite_format_tag = "format"
    # datacite_formats = []
    #
    # for resource in dataset.get("resources", []):
    #
    #     default_format = resource.get("mimetype", resource.get("mimetype_inner", ""))
    #     resource_format = resource.get("format", "")
    #
    #     if not resource_format:
    #         resource_format = default_format
    #
    #     if resource_format:
    #         datacite_format = {"#text": resource_format}
    #
    #         if datacite_format not in datacite_formats:
    #             datacite_formats += [datacite_format]
    #
    # if datacite_formats:
    #     datacite["resource"][datacite_format_group_tag] = {
    #         datacite_format_tag: datacite_formats
    #     }
    #
    # # Version
    # datacite_version_tag = "version"
    # datacite_version = dataset.get("version", "")
    # if datacite_version:
    #     datacite["resource"][datacite_version_tag] = {"#text": datacite_version}
    #
    # TODO extract rights block to separate function
    # # Rights
    # datacite_rights_group_tag = "rightsList"
    # datacite_rights_tag = "rights"
    # datacite_rights_uri_tag = "rightsURI"
    #
    # datacite_scheme_uri_tag = "schemeURI"
    # default_rights_scheme_uri = "https://spdx.org/licenses/"
    #
    # datacite_rights_identifier_scheme = "rightsIdentifierScheme"
    # default_rights_identifier = "SPDX"
    #
    # datacite_rights_identifier = "rightsIdentifier"  # "CC0 1.0"
    #
    # rights = {}
    #
    # rights_title = dataset.get("license_title", "")
    # if rights_title:
    #     rights = {f"@{datacite_xml_lang_tag}": "en-us", "#text": rights_title}
    #
    # rights_uri = dataset.get("license_url", "")
    # if rights_uri:
    #     rights[f"@{datacite_rights_uri_tag}"] = rights_uri
    #
    # license_id = dataset.get("license_id", "")
    #
    # rights_id_spx = value_to_datacite_cv(
    #     license_id, datacite_rights_identifier, default=None
    # )
    # if rights_id_spx:
    #     rights[f"@{datacite_scheme_uri_tag}"] = default_rights_scheme_uri
    #     rights[f"@{datacite_rights_identifier_scheme}"] = default_rights_identifier
    #     rights[f"@{datacite_rights_identifier}"] = rights_id_spx
    #
    # if rights:
    #     datacite["resource"][datacite_rights_group_tag] = {
    #         datacite_rights_tag: [rights]
    #     }
    #
    # TODO extract description block to separate function
    # # Description
    # datacite_descriptions_tag = "descriptions"
    # datacite_description_tag = "description"
    # datacite_description_type_tag = "descriptionType"
    # datacite_descriptions = []
    #
    # description = dataset.get("notes", "")
    # if description:
    #     description_text = (
    #         description.replace("\r", "")
    #         .replace(">", "-")
    #         .replace("<", "-")
    #         .replace("__", "")
    #         .replace("#", "")
    #         .replace("\n\n", "\n")
    #         .replace("\n\n", "\n")
    #     )
    #
    #     datacite_description = {
    #         "#text": description_text.strip(),
    #         f"@{datacite_description_type_tag}": "Abstract",
    #         f"@{datacite_xml_lang_tag}": "en-us",
    #     }
    #
    #     datacite_descriptions += [datacite_description]
    #
    # if datacite_descriptions:
    #     datacite["resource"][datacite_descriptions_tag] = {
    #         datacite_description_tag: datacite_descriptions
    #     }
    #
    # TODO separate geolocation block to separate function
    # # GeoLocation
    # datacite_geolocation_place_tag = "geoLocationPlace"
    #
    # datacite_geolocations = []
    # try:
    #     # Get spatial data from dataset
    #     pkg_spatial = json.loads(dataset["spatial"])
    #     log.debug("pkg_spatial=" + str(pkg_spatial))
    #     if pkg_spatial:
    #         coordinates = flatten(pkg_spatial.get("coordinates", "[]"), reverse=True)
    #         if pkg_spatial.get("type", "").lower() == "polygon":
    #             datacite_geolocation = collections.OrderedDict()
    #             datacite_geolocation["geoLocationPolygon"] = {"polygonPoint": []}
    #             for coordinates_pair in pkg_spatial.get("coordinates", "[[]]")[0]:
    #                 geolocation_point = collections.OrderedDict()
    #                 geolocation_point["pointLongitude"] = coordinates_pair[0]
    #                 geolocation_point["pointLatitude"] = coordinates_pair[1]
    #                 datacite_geolocation["geoLocationPolygon"]["polygonPoint"] += [
    #                     geolocation_point
    #                 ]
    #             datacite_geolocations += [datacite_geolocation]
    #         else:
    #             if pkg_spatial.get("type", "").lower() == "multipoint":
    #                 for coordinates_pair in pkg_spatial.get("coordinates", "[]"):
    #                     log.debug("point=" + str(coordinates_pair))
    #                     datacite_geolocation = collections.OrderedDict()
    #                     datacite_geolocation[
    #                         "geoLocationPoint"
    #                     ] = collections.OrderedDict()
    #                     datacite_geolocation["geoLocationPoint"][
    #                         "pointLongitude"
    #                     ] = coordinates_pair[0]
    #                     datacite_geolocation["geoLocationPoint"][
    #                         "pointLatitude"
    #                     ] = coordinates_pair[1]
    #                     datacite_geolocations += [datacite_geolocation]
    #             else:
    #                 datacite_geolocation = collections.OrderedDict()
    #                 datacite_geolocation["geoLocationPoint"] = collections.OrderedDict()
    #                 datacite_geolocation["geoLocationPoint"][
    #                     "pointLongitude"
    #                 ] = coordinates[1]
    #                 datacite_geolocation["geoLocationPoint"][
    #                     "pointLatitude"
    #                 ] = coordinates[0]
    #                 datacite_geolocations += [datacite_geolocation]
    # except JSONDecodeError:
    #     datacite_geolocations = []
    #
    # if datacite_geolocations:
    #
    #     geolocation_place = dataset.get("spatial_info", "")
    #     if geolocation_place:
    #         datacite_geolocation_place = {
    #             datacite_geolocation_place_tag: geolocation_place.strip()
    #         }
    #         datacite_geolocations += [datacite_geolocation_place]
    #
    #     datacite["resource"]["geoLocations"] = {"geoLocation": datacite_geolocations}
    #
    # TODO separate funding block to separate function
    # # Funding Information
    # datacite_funding_refs_tag = "fundingReferences"
    # datacite_funding_ref_tag = "fundingReference"
    #
    # datacite_funding_refs = []
    #
    # funding_dataset = dataset.get("funding", [])
    # try:
    #     funding = json.loads(funding_dataset)
    # except JSONDecodeError:
    #     funding = []
    #
    # for funder in funding:
    #
    #     datacite_funding_ref = collections.OrderedDict()
    #
    #     funder_name = funder.get("institution", "")
    #     if funder_name:
    #         datacite_funding_ref["funderName"] = funder_name.strip()
    #         award_number = funder.get("grant_number", "")
    #         if award_number:
    #             datacite_funding_ref["awardNumber"] = award_number.strip()
    #         datacite_funding_refs += [datacite_funding_ref]
    #
    # if datacite_funding_refs:
    #     datacite["resource"][datacite_funding_refs_tag] = {
    #         datacite_funding_ref_tag: datacite_funding_refs
    #     }

    return datacite


def get_datacite_creator(author: dict, config: dict):
    """Returns author information in DataCite "creator" tag format"""

    datacite_creator_tag = "creator"
    datacite_creator = collections.OrderedDict()

    creator_family_name = author.get(
        config[datacite_creator_tag]["familyName"], ""
    ).strip()
    creator_given_name = author.get(
        config[datacite_creator_tag]["givenName"], ""
    ).strip()

    if creator_given_name:
        datacite_creator["creatorName"] = f"{creator_given_name} {creator_family_name}"
        datacite_creator["givenName"] = creator_given_name
        datacite_creator["familyName"] = creator_family_name
    else:
        datacite_creator["creatorName"] = creator_family_name

    creator_identifier = author.get(config[datacite_creator_tag]["nameIdentifier"], "")
    if creator_identifier:
        datacite_creator["nameIdentifier"] = {
            "#text": creator_identifier.strip(),
            "@nameIdentifierScheme": "ORCID",
        }

    affiliations = []
    affiliation = author.get(config[datacite_creator_tag]["affiliation"], "")
    if affiliation:
        affiliations += [{"#text": affiliation.strip()}]

    affiliation_02 = author.get("affiliation_02", "")
    if affiliation_02:
        affiliations += [{"#text": affiliation_02.strip()}]

    affiliation_03 = author.get("affiliation_03", "")
    if affiliation_03:
        affiliations += [{"#text": affiliation_03.strip()}]

    if affiliations:
        datacite_creator["affiliation"] = affiliations

    return datacite_creator


def get_datacite_contributor(maintainer: dict, config: dict):
    """Returns maintainer information in DataCite "contributor" tag format"""

    datacite_contributor_tag = "contributor"

    datacite_contributor = collections.OrderedDict()

    contributor_family_name = maintainer.get(
        config[datacite_contributor_tag]["familyName"], ""
    ).strip()
    contributor_given_name = maintainer.get(
        config[datacite_contributor_tag]["givenName"], ""
    ).strip()

    if contributor_given_name:
        datacite_contributor[
            "contributorName"
        ] = f"{contributor_given_name} {contributor_family_name} "
        datacite_contributor["givenName"] = contributor_given_name
        datacite_contributor["familyName"] = contributor_family_name
    else:
        datacite_contributor["contributorName"] = contributor_family_name

    contributor_identifier = maintainer.get(
        config[datacite_contributor_tag]["nameIdentifier"], ""
    )
    if contributor_identifier:
        datacite_contributor["nameIdentifier"] = {
            "#text": contributor_identifier.strip(),
            "@nameIdentifierScheme": maintainer.get(
                join_tags(
                    [datacite_contributor_tag, "nameIdentifier", "nameIdentifierScheme"]
                ),
                "orcid",
            ).upper(),
        }

    contributor_affiliation = maintainer.get(
        config[datacite_contributor_tag]["affiliation"], ""
    )
    datacite_contributor["affiliation"] = contributor_affiliation.strip()

    contributor_type = maintainer.get(
        join_tags([datacite_contributor_tag, "contributorType"]), "ContactPerson"
    )
    datacite_contributor["@contributorType"] = value_to_datacite_cv(
        contributor_type, "contributorType"
    )

    return datacite_contributor


def datacite_convert_dataset(dataset: dict, name_doi_map: dict):
    """Convert EnviDat metadata package from CKAN to DataCite XML."""

    # Assign datacite to ordered dictionary that will contain
    # dataset content converted to DataCite format
    datacite = collections.OrderedDict()

    # Assign language tag used several times in function
    datacite_xml_lang_tag = "xml:lang"

    # Header
    datacite["resource"] = collections.OrderedDict()
    namespace = "http://datacite.org/schema/kernel-4"
    schema = "http://schema.datacite.org/meta/kernel-4.4/metadata.xsd"
    datacite["resource"]["@xsi:schemaLocation"] = f"{namespace} {schema}"
    datacite["resource"]["@xmlns"] = f"{namespace}"
    datacite["resource"]["@xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"

    # Identifier
    datacite_identifier_tag = "identifier"
    doi = dataset.get("doi", "")
    datacite["resource"][datacite_identifier_tag] = {
        "#text": doi.strip(),
        "@identifierType": "DOI",
    }

    # creators
    datacite_creators_tag = "creators"
    datacite_creator_tag = "creator"

    datacite["resource"][datacite_creators_tag] = {datacite_creator_tag: []}

    author_dataset = dataset.get("author", [])
    try:
        authors = json.loads(author_dataset)
    except JSONDecodeError:
        authors = []

    for author in authors:

        datacite_creator = collections.OrderedDict()

        creator_family_name = author.get("name", "").strip()
        creator_given_name = author.get("given_name", "").strip()

        if creator_given_name:
            datacite_creator[
                "creatorName"
            ] = f"{creator_given_name} {creator_family_name}"
            datacite_creator["givenName"] = creator_given_name
            datacite_creator["familyName"] = creator_family_name
        else:
            datacite_creator["creatorName"] = creator_family_name

        creator_identifier = author.get("identifier", "")
        if creator_identifier:
            datacite_creator["nameIdentifier"] = {
                "#text": creator_identifier.strip(),
                "@nameIdentifierScheme": "ORCID",
            }

        affiliations = []

        affiliation = author.get("affiliation", "")
        if affiliation:
            affiliations += [{"#text": affiliation.strip()}]

        affiliation_02 = author.get("affiliation_02", "")
        if affiliation_02:
            affiliations += [{"#text": affiliation_02.strip()}]

        affiliation_03 = author.get("affiliation_03", "")
        if affiliation_03:
            affiliations += [{"#text": affiliation_03.strip()}]

        if affiliations:
            datacite_creator["affiliation"] = affiliations

        datacite["resource"][datacite_creators_tag][datacite_creator_tag] += [
            datacite_creator
        ]

    # Titles
    datacite_titles_tag = "titles"
    datacite_title_tag = "title"
    datacite["resource"][datacite_titles_tag] = {datacite_title_tag: []}

    title = dataset.get("title", "")
    if title:
        datacite["resource"][datacite_titles_tag][datacite_title_tag] = {
            f"@{datacite_xml_lang_tag}": "en-us",
            "#text": title,
        }

    # Get publication dictionary
    pub = dataset.get("publication", {})
    try:
        publication = json.loads(pub)
    except JSONDecodeError:
        publication = {}

    # Publication year
    datacite_publication_year_tag = "publicationYear"

    publication_year = publication.get("publication_year", "")
    if publication_year:
        datacite["resource"][datacite_publication_year_tag] = {
            "#text": publication_year
        }

    # Publisher
    datacite_publisher_tag = "publisher"

    publisher = publication.get("publisher", "")
    if publisher:
        datacite["resource"][datacite_publisher_tag] = {
            f"@{datacite_xml_lang_tag}": "en-us",
            "#text": publisher.strip(),
        }

    # Subjects
    datacite_subjects = []

    # Get tags list
    tags = dataset.get("tags", [])

    for tag in tags:
        tag_name = tag.get("display_name", tag.get("name", ""))
        datacite_subjects += [{f"@{datacite_xml_lang_tag}": "en-us", "#text": tag_name}]

    if datacite_subjects:
        datacite_subjects_tag = "subjects"
        datacite_subject_tag = "subject"
        datacite["resource"][datacite_subjects_tag] = {
            datacite_subject_tag: datacite_subjects
        }

    # Contributor (contact person)
    datacite_contributors_tag = "contributors"
    datacite_contributor_tag = "contributor"

    maintainer_dataset = dataset.get("maintainer", {})
    try:
        maintainer = json.loads(maintainer_dataset)
    except JSONDecodeError:
        maintainer = {}

    datacite_contributor = collections.OrderedDict()

    contributor_family_name = maintainer.get("name", "").strip()
    contributor_given_name = maintainer.get("given_name", "").strip()

    if contributor_given_name:
        datacite_contributor[
            "contributorName"
        ] = f"{contributor_given_name} {contributor_family_name}"
        datacite_contributor["givenName"] = contributor_given_name
        datacite_contributor["familyName"] = contributor_family_name
    else:
        datacite_contributor["contributorName"] = contributor_family_name

    contributor_identifier = maintainer.get("identifier", "")
    if contributor_identifier:
        datacite_contributor["nameIdentifier"] = {
            "#text": contributor_identifier.strip(),
            "@nameIdentifierScheme": maintainer.get(
                join_tags(
                    [datacite_contributor_tag, "nameIdentifier", "nameIdentifierScheme"]
                ),
                "orcid",
            ).upper(),
        }

    contributor_affiliation = maintainer.get("affiliation", "")
    datacite_contributor["affiliation"] = contributor_affiliation.strip()

    contributor_type = maintainer.get(
        join_tags([datacite_contributor_tag, "contributorType"]), "ContactPerson"
    )
    datacite_contributor["@contributorType"] = value_to_datacite_cv(
        contributor_type, "contributorType"
    )

    if datacite_contributor:
        datacite["resource"][datacite_contributors_tag] = {
            datacite_contributor_tag: datacite_contributor
        }

    # Dates
    datacite_dates_tag = "dates"
    datacite_date_tag = "date"
    datacite_date_type_tag = "dateType"
    datacite_dates = []

    date_input = dataset.get("date", [])
    try:
        dates = json.loads(date_input)
    except JSONDecodeError:
        dates = []

    for date in dates:
        datacite_date = {
            "#text": date.get("date", ""),
            f"@{datacite_date_type_tag}": (date.get("date_type", "Valid")).title(),
        }
        datacite_dates += [datacite_date]

    if datacite_dates:
        datacite["resource"][datacite_dates_tag] = {datacite_date_tag: datacite_dates}

    # Language
    datacite_language_tag = "language"
    datacite_language = dataset.get("language", "")
    if not datacite_language:
        datacite_language = "en"
    datacite["resource"][datacite_language_tag] = {"#text": datacite_language}

    # ResourceType
    datacite_resource_type_tag = "resourceType"
    datacite_resource_type_general_tag = "resourceTypeGeneral"
    resource_type_general = dataset.get("resource_type_general", "Dataset")
    datacite_resource_type_general = value_to_datacite_cv(
        resource_type_general, datacite_resource_type_general_tag, default="Dataset"
    )

    datacite["resource"][datacite_resource_type_tag] = {
        "#text": dataset.get("resource_type", ""),
        # f'@{datacite_resource_type_general_tag}': (
        #     dataset.get('resource_type_general', 'Dataset'
        # )).title()
        f"@{datacite_resource_type_general_tag}": datacite_resource_type_general,
    }

    # Alternate Identifier
    base_url = "https://www.envidat.ch/dataset/"
    alternate_identifiers = []

    package_name = dataset.get("name", "")
    if package_name:
        package_url = f"{base_url}{package_name}"
        alternate_identifiers.append(
            {"#text": package_url, "@alternateIdentifierType": "URL"}
        )

    package_id = dataset.get("id", "")
    if package_id:
        package_id = f"{base_url}{package_id}"
        alternate_identifiers.append(
            {"#text": package_id, "@alternateIdentifierType": "URL"}
        )

    datacite["resource"]["alternateIdentifiers"] = {
        "alternateIdentifier": alternate_identifiers
    }

    # Related identifier
    datacite_related_urls = collections.OrderedDict()
    datacite_related_urls["relatedIdentifier"] = []

    # Combine "related_publications" and "related_datasets" values
    related_publications = dataset.get("related_publications", "")
    related_datasets = dataset.get("related_datasets", "")
    related_identifiers = f"${related_publications} {related_datasets}"

    # Validate related_identifiers
    if len(related_identifiers) > 0:
        # Remove special characters "\r", "\n" and
        # remove Markdown link syntax using brackets and parentheses
        # and replace with one space " "
        related_identifiers = re.sub(r"\r|\n|\[|\]|\(|\)", " ", related_identifiers)

        # Assign empty array to hold "related_ids" values that will be used to check for
        # duplicates
        related_ids = []

        for word in related_identifiers.split(" "):

            # Apply search function to find DOIs
            doi = get_doi(word)

            # Apply search criteria to find DOIs from DORA API
            # DORA API documentation:
            # https://www.wiki.lib4ri.ch/display/HEL/Technical+details+of+DORA
            dora_str = "dora.lib4ri.ch/wsl/islandora/object/"
            if dora_str in word:
                dora_index = word.find(dora_str)
                dora_pid = word[(dora_index + len(dora_str)) :]

                # Call DORA API and get DOI if it listed in citation
                doi_dora = get_dora_doi(dora_pid)
                if doi_dora:
                    doi = doi_dora

            if doi and "/" in doi and doi not in related_ids:
                related_ids.append(doi)
                datacite_related_urls["relatedIdentifier"] += [
                    {
                        "#text": doi,
                        "@relatedIdentifierType": "DOI",
                        "@relationType": "isSupplementTo",
                    }
                ]
                continue

            # Apply URL validator to find other URLs (that are not DOIs)
            is_url = validators.url(word)

            if all([is_url, word not in related_ids, "doi" not in word]):
                related_ids.append(word)

                # EnviDat datasets are assigned a relationType of "Cites"
                if word.startswith(
                    ("https://envidat.ch/#/metadata/", "https://envidat.ch/dataset/")
                ):
                    datacite_related_urls["relatedIdentifier"] += [
                        {
                            "#text": word,
                            "@relatedIdentifierType": "URL",
                            "@relationType": "Cites",
                        }
                    ]
                else:
                    # All other URLs are assigned a relationType of "isSupplementTo"
                    datacite_related_urls["relatedIdentifier"] += [
                        {
                            "#text": word,
                            "@relatedIdentifierType": "URL",
                            "@relationType": "isSupplementTo",
                        }
                    ]

    if len(datacite_related_urls["relatedIdentifier"]) > 0:
        datacite["resource"]["relatedIdentifiers"] = datacite_related_urls

    # Sizes (from resources)
    datacite_size_group_tag = "sizes"
    datacite_size_tag = "size"
    datacite_sizes = []

    for resource in dataset.get("resources", []):
        if resource.get("size", ""):
            datacite_sizes += [{"#text": str(resource.get("size", " ")) + " bytes"}]
        elif resource.get("resource_size", ""):
            resource_size = resource.get("resource_size", "")
            try:
                resource_size_obj = json.loads(resource_size)
                datacite_sizes += [
                    {
                        "#text": (
                            resource_size_obj.get("size_value", "0")
                            + " "
                            + resource_size_obj.get("size_unit", "KB").upper()
                        ).strip()
                    }
                ]
            except JSONDecodeError:
                log.error("non-parsable value at resource_size:" + str(resource_size))

    if datacite_sizes:
        datacite["resource"][datacite_size_group_tag] = {
            datacite_size_tag: datacite_sizes
        }

    # Formats (from resources)
    datacite_format_group_tag = "formats"
    datacite_format_tag = "format"
    datacite_formats = []

    for resource in dataset.get("resources", []):

        default_format = resource.get("mimetype", resource.get("mimetype_inner", ""))
        resource_format = resource.get("format", "")

        if not resource_format:
            resource_format = default_format

        if resource_format:
            datacite_format = {"#text": resource_format}

            if datacite_format not in datacite_formats:
                datacite_formats += [datacite_format]

    if datacite_formats:
        datacite["resource"][datacite_format_group_tag] = {
            datacite_format_tag: datacite_formats
        }

    # Version
    datacite_version_tag = "version"
    datacite_version = dataset.get("version", "")
    if datacite_version:
        datacite["resource"][datacite_version_tag] = {"#text": datacite_version}

    # Rights
    datacite_rights_group_tag = "rightsList"
    datacite_rights_tag = "rights"
    datacite_rights_uri_tag = "rightsURI"

    datacite_scheme_uri_tag = "schemeURI"
    default_rights_scheme_uri = "https://spdx.org/licenses/"

    datacite_rights_identifier_scheme = "rightsIdentifierScheme"
    default_rights_identifier = "SPDX"

    datacite_rights_identifier = "rightsIdentifier"  # "CC0 1.0"

    rights = {}

    rights_title = dataset.get("license_title", "")
    if rights_title:
        rights = {f"@{datacite_xml_lang_tag}": "en-us", "#text": rights_title}

    rights_uri = dataset.get("license_url", "")
    if rights_uri:
        rights[f"@{datacite_rights_uri_tag}"] = rights_uri

    license_id = dataset.get("license_id", "")

    rights_id_spx = value_to_datacite_cv(
        license_id, datacite_rights_identifier, default=None
    )
    if rights_id_spx:
        rights[f"@{datacite_scheme_uri_tag}"] = default_rights_scheme_uri
        rights[f"@{datacite_rights_identifier_scheme}"] = default_rights_identifier
        rights[f"@{datacite_rights_identifier}"] = rights_id_spx

    if rights:
        datacite["resource"][datacite_rights_group_tag] = {
            datacite_rights_tag: [rights]
        }

    # Description
    datacite_descriptions_tag = "descriptions"
    datacite_description_tag = "description"
    datacite_description_type_tag = "descriptionType"
    datacite_descriptions = []

    description = dataset.get("notes", "")
    if description:
        description_text = (
            description.replace("\r", "")
            .replace(">", "-")
            .replace("<", "-")
            .replace("__", "")
            .replace("#", "")
            .replace("\n\n", "\n")
            .replace("\n\n", "\n")
        )

        datacite_description = {
            "#text": description_text.strip(),
            f"@{datacite_description_type_tag}": "Abstract",
            f"@{datacite_xml_lang_tag}": "en-us",
        }

        datacite_descriptions += [datacite_description]

    if datacite_descriptions:
        datacite["resource"][datacite_descriptions_tag] = {
            datacite_description_tag: datacite_descriptions
        }

    # GeoLocation
    datacite_geolocation_place_tag = "geoLocationPlace"

    datacite_geolocations = []
    try:
        # Get spatial data from dataset
        pkg_spatial = json.loads(dataset["spatial"])
        log.debug("pkg_spatial=" + str(pkg_spatial))
        if pkg_spatial:
            coordinates = flatten(pkg_spatial.get("coordinates", "[]"), reverse=True)
            if pkg_spatial.get("type", "").lower() == "polygon":
                datacite_geolocation = collections.OrderedDict()
                datacite_geolocation["geoLocationPolygon"] = {"polygonPoint": []}
                for coordinates_pair in pkg_spatial.get("coordinates", "[[]]")[0]:
                    geolocation_point = collections.OrderedDict()
                    geolocation_point["pointLongitude"] = coordinates_pair[0]
                    geolocation_point["pointLatitude"] = coordinates_pair[1]
                    datacite_geolocation["geoLocationPolygon"]["polygonPoint"] += [
                        geolocation_point
                    ]
                datacite_geolocations += [datacite_geolocation]
            else:
                if pkg_spatial.get("type", "").lower() == "multipoint":
                    for coordinates_pair in pkg_spatial.get("coordinates", "[]"):
                        log.debug("point=" + str(coordinates_pair))
                        datacite_geolocation = collections.OrderedDict()
                        datacite_geolocation[
                            "geoLocationPoint"
                        ] = collections.OrderedDict()
                        datacite_geolocation["geoLocationPoint"][
                            "pointLongitude"
                        ] = coordinates_pair[0]
                        datacite_geolocation["geoLocationPoint"][
                            "pointLatitude"
                        ] = coordinates_pair[1]
                        datacite_geolocations += [datacite_geolocation]
                else:
                    datacite_geolocation = collections.OrderedDict()
                    datacite_geolocation["geoLocationPoint"] = collections.OrderedDict()
                    datacite_geolocation["geoLocationPoint"][
                        "pointLongitude"
                    ] = coordinates[1]
                    datacite_geolocation["geoLocationPoint"][
                        "pointLatitude"
                    ] = coordinates[0]
                    datacite_geolocations += [datacite_geolocation]
    except JSONDecodeError:
        datacite_geolocations = []

    if datacite_geolocations:

        geolocation_place = dataset.get("spatial_info", "")
        if geolocation_place:
            datacite_geolocation_place = {
                datacite_geolocation_place_tag: geolocation_place.strip()
            }
            datacite_geolocations += [datacite_geolocation_place]

        datacite["resource"]["geoLocations"] = {"geoLocation": datacite_geolocations}

    # Funding Information
    datacite_funding_refs_tag = "fundingReferences"
    datacite_funding_ref_tag = "fundingReference"

    datacite_funding_refs = []

    funding_dataset = dataset.get("funding", [])
    try:
        funding = json.loads(funding_dataset)
    except JSONDecodeError:
        funding = []

    for funder in funding:

        datacite_funding_ref = collections.OrderedDict()

        funder_name = funder.get("institution", "")
        if funder_name:
            datacite_funding_ref["funderName"] = funder_name.strip()
            award_number = funder.get("grant_number", "")
            if award_number:
                datacite_funding_ref["awardNumber"] = award_number.strip()
            datacite_funding_refs += [datacite_funding_ref]

    if datacite_funding_refs:
        datacite["resource"][datacite_funding_refs_tag] = {
            datacite_funding_ref_tag: datacite_funding_refs
        }

    return datacite


def flatten(inp: list, reverse: bool = False) -> list:
    """Flatten list, i.e. remove a dimension/nesting."""
    output = []
    for item in inp:
        if type(item) is not list:
            if reverse:
                output = [str(item)] + output
            else:
                output += [str(item)]
        else:
            output += flatten(item, reverse)
    return output


def join_tags(tags: list, sep: str = ".") -> str:
    """Join tags by a provided separator."""
    return sep.join([tag for tag in tags if tag])


def value_to_datacite_cv(value: str, datacite_tag: str, default: str = "") -> dict:
    """Constant definitions."""
    datacite_cv = {
        "titleType": {
            "alternativetitle": "AlternativeTitle",
            "subtitle": "Subtitle",
            "translatedtitle": "TranslatedTitle",
            "other": "Other",
        },
        "resourceTypeGeneral": {
            "audiovisual": "Audiovisual",
            "collection": "Collection",
            "dataset": "Dataset",
            "event": "Event",
            "image": "Image",
            "interactiveresource": "InteractiveResource",
            "model": "Model",
            "physicalobject": "PhysicalObject",
            "service": "Service",
            "software": "Software",
            "sound": "Sound",
            "text": "Text",
            "workflow": "Workflow",
            "other": "Other",
        },
        "descriptionType": {
            "abstract": "Abstract",
            "methods": "Methods",
            "seriesinformation": "SeriesInformation",
            "tableofcontents": "TableOfContents",
            "other": "Other",
        },
        "contributorType": {
            "contactperson": "ContactPerson",
            "datacollector": "DataCollector",
            "datacurator": "DataCurator",
            "datamanager": "DataManager",
            "distributor": "Distributor",
            "editor": "Editor",
            "funder": "Funder",
            "hostinginstitution": "HostingInstitution",
            "other": "Other",
            "producer": "Producer",
            "projectleader": "ProjectLeader",
            "projectmanager": "ProjectManager",
            "projectmember": "ProjectMember",
            "registrationagency": "RegistrationAgency",
            "registrationauthority": "RegistrationAuthority",
            "relatedperson": "RelatedPerson",
            "researchgroup": "ResearchGroup",
            "rightsholder": "RightsHolder",
            "researcher": "Researcher",
            "sponsor": "Sponsor",
            "supervisor": "Supervisor",
            "workpackageleader": "WorkPackageLeader",
        },
        "rightsIdentifier": {
            "odc-odbl": "ODbL-1.0",
            "cc-by-sa": "CC-BY-SA-4.0",
            "cc-by-nc": "CC-BY-NC-4.0",
        },
    }

    # Matching ignoring blanks, case, symbols
    value_to_match = value.lower().replace(" ", "").replace("_", "")
    match_cv = datacite_cv.get(datacite_tag, {}).get(value_to_match, default)

    return match_cv


# TODO removed unused legacy function
# FIELD_NAME = "field_name"
# def map_fields(schema: dict, format_name: str) -> dict:
#     """Map fields into correct formatting."""
#     fields_map = {}
#     for field in schema:
#         format_field = ""
#         if field.get(format_name, False):
#             format_field = field[format_name]
#             fields_map[format_field] = {FIELD_NAME: field[FIELD_NAME], "subfields": {}}
#         for subfield in field.get("subfields", []):
#             if subfield.get(format_name, False):
#                 format_subfield = subfield[format_name]
#                 if format_field:
#                     if not fields_map[format_field]["subfields"].get(
#                         format_subfield, False
#                     ):
#                         fields_map[format_field]["subfields"][format_subfield] = {
#                             FIELD_NAME: subfield[FIELD_NAME]
#                         }
#                     else:
#                         value = fields_map[format_field]["subfields"][format_subfield][
#                             FIELD_NAME
#                         ]
#                         if isinstance(value, list):
#                             fields_map[format_field]["subfields"][format_subfield] = {
#                                 FIELD_NAME: value + [subfield[FIELD_NAME]]
#                             }
#                         else:
#                             fields_map[format_field]["subfields"][format_subfield] = {
#                                 FIELD_NAME: [value, subfield[FIELD_NAME]]
#                             }
#                 else:
#                     fields_map[format_subfield] = {
#                         FIELD_NAME: field[FIELD_NAME] + "." + subfield[FIELD_NAME]
#                     }
#     return fields_map


def get_doi(word: str):
    """Get DOI string from input word string, if DOI not found then returns None

    For example: an input of "https://doi.org/10.1525/cse.2022.1561651" would return
        "10.1525/cse.2022.1561651" as output

    Args:
        word (str): Input string to test if it contains a DOI

    Returns:
        str: String of DOI
        None: If DOI could not be found
    """

    doi = None

    # Apply search criteria to find DOIs
    if "doi" in word:
        doi_start_index = word.find("10.")
        doi = word[doi_start_index:]

    # Return DOI if it exists, else return None
    return doi


def get_dora_doi(dora_pid: str, host: str = "https://envidat.ch", path: str = "/dora"):
    """Get DOI string from WSL DORA API using DORA PID

    DORA API documentation:
    https://www.wiki.lib4ri.ch/display/HEL/Technical+details+of+DORA

    ASSUMPTION: Only one DOI exists in each DORA API record "citation" key

    Args:
        dora_pid (str): DORA PID (permanent identification)
        host (str): API host url. Attempts to get from environment if omitted.
            Defaults to "https://www.envidat.ch"
        path (str): API host path. Attempts to get from environment if omitted.
            Defaults to "/dora"

    Returns:
        str: String of DOI
        None: If DOI could not be found
    """
    if "API_HOST" in os.environ and "API_ENVIDAT_DORA" in os.environ:
        log.debug("Getting API host and path from environment variables.")
        host = os.getenv("API_HOST")
        path = os.getenv("API_ENVIDAT_DORA")

    # Replace '%3A' ASCII II code with semicolon ':'
    dora_pid = re.sub("%3A", ":", dora_pid)

    # Assemble url used to call DORA API
    dora_url = f"{host}{path}/{dora_pid}"

    try:
        data = get_url(dora_url).json()
        citation = data[dora_pid]["citation"]["ACS"]

        for word in citation.split(" "):
            doi = get_doi(word)

            # Return DOI if it exists
            if doi:
                return doi

        # If DOI not found then return None
        return None

    except Exception as e:
        print(f"ERROR: Failed to retrieve'{dora_url}' and extract DOI")
        print(e)

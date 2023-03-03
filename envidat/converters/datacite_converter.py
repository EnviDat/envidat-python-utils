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


def convert_datacite(metadata_record: dict) -> str:
    """Generate XML formatted string in DataCite format.

    Note:
        Converter is only valid for the metadata schema for EnviDat.

    Args:
        metadata_record (dict): Individual EnviDat metadata entry record dictionary.

    Returns:
        str: XML formatted string compatible with DataCite DIF 10.2 standard
    """
    try:
        # TODO finish refactoring Datacite converter
        config: dict = get_config_datacite_converter()
        converted_package = datacite_convert_dataset(metadata_record, config)
        return unparse(converted_package, pretty=True)  # Convert OrderedDict to XML
    except ValueError as e:
        log.error(e)
        log.error("Cannot convert package to DataCite format.")
        raise ValueError("Failed to convert package to DataCite format.")


# TODO possibly implement JSON schema to make sure all required keys included in config,
#  see https://pypi.org/project/jsonschema/ and
#  https://towardsdatascience.com/how-to-use-json-schema-to-validate-json-documents
#  -ae9d8d1db344
# TODO move "envidat/converters/config_converters.json" to "config" directory
def get_config_datacite_converter(
        config_path: str = "envidat/converters/config_converters.json"
) -> dict:
    """Return datacite converter JSON config as Python dictionary.

    Dictionary maps Datacite XML schema tags (keys) to EnviDat schema fields (values).

    Args:
        config_path (str): Path to JSON config file,
                           default path is "envidat/converters/config_converters.json"

    Returns:
        dict: datacite converter JSON config as Python dictionary

    """
    with open(config_path, encoding='utf-8') as config_json:
        config: dict = json.load(config_json)
        datacite_config: dict = config["datacite_converter"]
    return datacite_config


# TODO connect DataCite converter to DOI CKAN extension
# TODO keep in mind that a reverse converter will
#  also need to be written (Datacite to EnviDat)
# TODO write docstring
def datacite_convert_dataset(dataset: dict, config: dict):
    """Convert EnviDat metadata package from CKAN to DataCite XML.

       Notes: This converter is compatible with DataCite Metadata Schema 4.4, for
       documentation see https://schema.datacite.org/meta/kernel-4.4/
    """

    # Initialize ordered dictionary that will contain
    # dataset content converted to DataCite format
    dc = collections.OrderedDict()

    # Assign language tag used several times in function
    dc_xml_lang_tag = "xml:lang"

    # Header
    dc["resource"] = collections.OrderedDict()
    namespace = "http://datacite.org/schema/kernel-4"
    schema = "http://schema.datacite.org/meta/kernel-4.4/metadata.xsd"
    dc["resource"]["@xsi:schemaLocation"] = f"{namespace} {schema}"
    dc["resource"]["@xmlns"] = f"{namespace}"
    dc["resource"]["@xmlns:xsi"] = "http://www.w3.org/2001/XMLSchema-instance"

    # Identifier
    dc_identifier_tag = "identifier"
    doi = dataset.get(config[dc_identifier_tag], "")
    dc["resource"][dc_identifier_tag] = {
        "#text": doi.strip(),
        "@identifierType": "DOI",
    }

    # Creators
    dc_creators_tag = "creators"
    dc_creator_tag = "creator"
    dc["resource"][dc_creators_tag] = {dc_creator_tag: []}
    author_dataset = dataset.get(config[dc_creators_tag], [])
    try:
        authors = json.loads(author_dataset)
    except JSONDecodeError:
        authors = []

    for author in authors:
        dc_creator = get_dc_creator(author, config)
        dc["resource"][dc_creators_tag][dc_creator_tag] += [dc_creator]

    # Titles
    dc_titles_tag = "titles"
    dc_title_tag = "title"
    dc["resource"][dc_titles_tag] = {dc_title_tag: []}
    title = dataset.get(config[dc_title_tag], "")
    if title:
        dc["resource"][dc_titles_tag][dc_title_tag] = {
            f"@{dc_xml_lang_tag}": "en-us",
            "#text": title,
        }

    # Get publication dictionary
    pub = dataset.get("publication", {})
    try:
        publication = json.loads(pub)
    except JSONDecodeError:
        publication = {}

    # Publication year
    dc_publication_year_tag = "publicationYear"
    publication_year = publication.get(config[dc_publication_year_tag], "")
    if publication_year:
        dc["resource"][dc_publication_year_tag] = {"#text": publication_year}

    # Publisher
    dc_publisher_tag = "publisher"
    publisher = publication.get(config[dc_publisher_tag], "")
    if publisher:
        dc["resource"][dc_publisher_tag] = {
            f"@{dc_xml_lang_tag}": "en-us",
            "#text": publisher.strip(),
        }

    # Subjects
    dc_subjects_tag = "subjects"
    dc_subject_tag = "subject"
    dc_subjects = []

    tags = dataset.get(config[dc_subjects_tag], [])
    for tag in tags:
        tag_name = tag.get(config[dc_subject_tag], tag.get("name", ""))
        if tag_name:
            dc_subjects += [{f"@{dc_xml_lang_tag}": "en-us", "#text": tag_name}]

    if dc_subjects:
        dc["resource"][dc_subjects_tag] = {dc_subject_tag: dc_subjects}

    # Contributor (contact person)
    dc_contributors_tag = "contributors"
    dc_contributor_tag = "contributor"
    dc["resource"][dc_contributors_tag] = {dc_contributor_tag: []}

    # Get "maintainer" from EnviDat package,
    # assigned as DataCite Contributor "ContactPerson"
    maintainer_dataset = dataset.get(config[dc_contributors_tag], {})
    try:
        maintainer = json.loads(maintainer_dataset)
    except JSONDecodeError:
        maintainer = {}

    dc_contributor = get_dc_contributor(maintainer, config)
    if dc_contributor:
        dc["resource"][dc_contributors_tag][dc_contributor_tag] += [dc_contributor]

    # Get "organization" dataset and extract "name" value,
    # assigned as DataCite Contributor "ResearchGroup"
    organization = dataset.get("organization", {})
    if organization:
        organization_title = organization.get("title", "")
        if organization_title:
            dc_research_group = get_dc_research_group(organization_title)
            dc["resource"][dc_contributors_tag][dc_contributor_tag] \
                += [dc_research_group]

    # Dates
    dc_dates_tag = "dates"
    dc_date_tag = "date"
    dc_date_type_tag = "dateType"
    dc_dates = []

    date_input = dataset.get(config[dc_dates_tag], [])
    try:
        dates = json.loads(date_input)
    except JSONDecodeError:
        dates = []

    for date in dates:
        dc_date = {
            "#text": date.get(config[dc_date_tag], ""),
            f"@{dc_date_type_tag}": (
                date.get(config[dc_date_type_tag], "Valid")
            ).title(),
        }
        dc_dates += [dc_date]

    if dc_dates:
        dc["resource"][dc_dates_tag] = {dc_date_tag: dc_dates}

    # Language, "en" (English is default langauge)
    dc_language_tag = "language"
    dc_language = dataset.get(config[dc_language_tag], "")
    if not dc_language:
        dc_language = "en"
    dc["resource"][dc_language_tag] = {"#text": dc_language}

    # ResourceType
    dc_resource_type_tag = "resourceType"
    dc_resource_type_general_tag = "resourceTypeGeneral"
    resource_type_general = dataset.get(config[dc_resource_type_general_tag], "Dataset")
    dc_resource_type_general = value_to_datacite_cv(
        resource_type_general, dc_resource_type_general_tag, default="Dataset"
    )

    dc["resource"][dc_resource_type_tag] = {
        "#text": dataset.get(config[dc_resource_type_tag], ""),
        f"@{dc_resource_type_general_tag}": dc_resource_type_general,
    }

    # Alternate Identifier
    base_url = "https://www.envidat.ch/#/metadata/"
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

    dc["resource"]["alternateIdentifiers"] = {
        "alternateIdentifier": alternate_identifiers
    }

    # Get "resources" from EnviDat package,
    # used for DataCite "relatedIdentifiers" and "formats" tags
    resources = dataset.get("resources", [])

    # Related identifier
    # Combine "related_publications" and "related_datasets" values
    # Note: EnviDat keys hard-coded because DataCite "relatedIdentifier" tags
    # combines two EnviDat fields
    related_publications = dataset.get("related_publications", "")
    related_datasets = dataset.get("related_datasets", "")
    related_identifiers = f"${related_publications} {related_datasets}"

    dc_related_identifiers = get_dc_related_identifiers(related_identifiers, resources)
    if len(dc_related_identifiers["relatedIdentifier"]) > 0:
        dc["resource"]["relatedIdentifiers"] = dc_related_identifiers

    # Formats (from resources)
    dc_formats = get_dc_formats(resources)
    if dc_formats:
        dc_format_group_tag = "formats"
        dc_format_tag = "format"
        dc["resource"][dc_format_group_tag] = {dc_format_tag: dc_formats}

    # Version
    dc_version_tag = "version"
    dc_version = dataset.get(config[dc_version_tag], "")
    if dc_version:
        dc["resource"][dc_version_tag] = {"#text": dc_version}

    # Rights
    dc_rights_group_tag = "rightsList"
    dc_rights_tag = "rights"
    dc_rights_uri_tag = "rightsURI"

    dc_scheme_uri_tag = "schemeURI"
    default_rights_scheme_uri = "https://spdx.org/licenses/"

    dc_rights_identifier_scheme = "rightsIdentifierScheme"
    default_rights_identifier = "SPDX"

    dc_rights_identifier = "rightsIdentifier"  # "CC0 1.0"

    rights = {}

    dc_rights_text = "#text"
    rights_title = dataset.get(config[dc_rights_tag][dc_rights_text], "")
    if rights_title:
        rights = {f"@{dc_xml_lang_tag}": "en-us", "#text": rights_title}

    rights_uri = dataset.get(config[dc_rights_tag][dc_rights_uri_tag], "")
    if rights_uri:
        rights[f"@{dc_rights_uri_tag}"] = rights_uri

    license_id = dataset.get(config[dc_rights_tag][dc_rights_identifier], "")
    # TODO investigate default argument
    rights_id_spx = value_to_datacite_cv(license_id, dc_rights_identifier, default=None)
    if rights_id_spx:
        rights[f"@{dc_scheme_uri_tag}"] = default_rights_scheme_uri
        rights[f"@{dc_rights_identifier_scheme}"] = default_rights_identifier
        rights[f"@{dc_rights_identifier}"] = rights_id_spx

    if rights:
        dc["resource"][dc_rights_group_tag] = {dc_rights_tag: [rights]}

    # Description
    dc_descriptions_tag = "descriptions"
    dc_description_tag = "description"
    dc_description_type_tag = "descriptionType"

    notes = dataset.get(config[dc_description_tag], "")
    dc_descriptions = get_dc_descriptions(
        notes, dc_description_type_tag, dc_xml_lang_tag
    )

    if dc_descriptions:
        dc["resource"][dc_descriptions_tag] = {dc_description_tag: dc_descriptions}

    # GeoLocation
    dc_geolocations_tag = "geoLocations"
    dc_geolocations = []

    # Get spatial data from dataset
    try:
        spatial = json.loads(dataset.get(config[dc_geolocations_tag], ""))
        if spatial:
            dc_geolocations = get_dc_geolocations(spatial)
    except JSONDecodeError:
        dc_geolocations = []

    # Assign converted spatial and spatial_info values to corresponding DataCite tags
    if dc_geolocations:
        dc_geolocation_place_tag = "geoLocationPlace"

        geolocation_place = dataset.get(config[dc_geolocation_place_tag], "")
        if geolocation_place:
            datacite_geolocation_place = {
                dc_geolocation_place_tag: geolocation_place.strip()
            }
            dc_geolocations += [datacite_geolocation_place]

        dc["resource"][dc_geolocations_tag] = {"geoLocation": dc_geolocations}

    # Funding Information
    dc_funding_refs_tag = "fundingReferences"
    dc_funding_ref_tag = "fundingReference"

    funding_dataset = dataset.get(config[dc_funding_refs_tag], [])
    try:
        funding = json.loads(funding_dataset)
    except JSONDecodeError:
        funding = []

    dc_funding_refs = []

    for funder in funding:

        dc_funding_ref = collections.OrderedDict()
        dc_funder_name_tag = "funderName"

        funder_name = funder.get(config[dc_funding_ref_tag][dc_funder_name_tag], "")
        if funder_name:
            dc_funding_ref[dc_funder_name_tag] = funder_name.strip()

            dc_award_number_tag = "awardNumber"
            award_number = funder.get(
                config[dc_funding_ref_tag][dc_award_number_tag], ""
            )

            dc_award_uri_tag = "awardURI"
            award_uri = funder.get(config[dc_funding_ref_tag][dc_award_uri_tag], "")

            # TODO test new "awardURI" tag with DataCite test API
            # Assign awardNumber and awardURI if they exist
            # NOTE: For reverse converter be sure to parse default value for
            # awardNumber, ":unav"
            # DataCite documentation for unknown information: p. 74
            # https://schema.datacite.org/meta/kernel-4.4/doc/DataCite
            # -MetadataKernel_v4.4.pdf
            if award_uri:
                if award_number:
                    award = {f"@{dc_award_uri_tag}": award_uri,
                             "#text": award_number.strip()}
                else:
                    award = {f"@{dc_award_uri_tag}": award_uri, "#text": ":unav"}
                dc_funding_ref[dc_award_number_tag] = award
            elif award_number:
                dc_funding_ref[dc_award_number_tag] = award_number.strip()

            dc_funding_refs += [dc_funding_ref]

    if dc_funding_refs:
        dc["resource"][dc_funding_refs_tag] = {
            dc_funding_ref_tag: dc_funding_refs
        }

    return dc


# TODO research if author email can/should be included
def get_dc_creator(author: dict, config: dict):
    """Returns author information in DataCite "creator" tag format"""

    dc_creator_tag = "creator"
    dc_creator = collections.OrderedDict()

    creator_family_name = author.get(config[dc_creator_tag]["familyName"], "").strip()
    creator_given_name = author.get(config[dc_creator_tag]["givenName"], "").strip()

    if creator_given_name:
        dc_creator["creatorName"] = f"{creator_given_name} {creator_family_name}"
        dc_creator["givenName"] = creator_given_name
        dc_creator["familyName"] = creator_family_name
    else:
        dc_creator["creatorName"] = creator_family_name

    creator_identifier = author.get(config[dc_creator_tag]["nameIdentifier"], "")
    if creator_identifier:
        dc_creator["nameIdentifier"] = {
            "#text": creator_identifier.strip(),
            "@nameIdentifierScheme": "ORCID",
            "@schemeURI": "https://orcid.org/"
        }

    affiliations = []
    affiliation = author.get(config[dc_creator_tag]["affiliation"], "")
    if affiliation:
        aff = affiliation_to_dc(affiliation, config)
        affiliations += [aff]

    affiliation_02 = author.get("affiliation_02", "")
    if affiliation_02:
        aff_02 = affiliation_to_dc(affiliation_02, config)
        affiliations += [aff_02]

    affiliation_03 = author.get("affiliation_03", "")
    if affiliation_03:
        aff_03 = affiliation_to_dc(affiliation_03, config)
        affiliations += [aff_03]

    if affiliations:
        dc_creator["affiliation"] = affiliations

    return dc_creator


def get_dc_contributor(maintainer: dict, config: dict):
    """Returns maintainer in DataCite "contributor" tag format with a
    contributorType of "ContactPerson" """

    dc_contributor = collections.OrderedDict()
    dc_contributor_tag = "contributor"

    contributor_family_name = maintainer.get(
        config[dc_contributor_tag]["familyName"], ""
    ).strip()
    contributor_given_name = maintainer.get(
        config[dc_contributor_tag]["givenName"], ""
    ).strip()

    if contributor_given_name:
        dc_contributor[
            "contributorName"] = f"{contributor_given_name} {contributor_family_name}"
        dc_contributor["givenName"] = contributor_given_name
        dc_contributor["familyName"] = contributor_family_name
    else:
        dc_contributor["contributorName"] = contributor_family_name

    contributor_identifier = maintainer.get(
        config[dc_contributor_tag]["nameIdentifier"], ""
    )
    if contributor_identifier:
        dc_contributor["nameIdentifier"] = {
            "#text": contributor_identifier.strip(),
            "@nameIdentifierScheme": maintainer.get(
                join_tags(
                    [dc_contributor_tag, "nameIdentifier", "nameIdentifierScheme"]
                ),
                "orcid",
            ).upper(),
            "@schemeURI": "https://orcid.org/"
        }

    contributor_affiliation = maintainer.get(
        config[dc_contributor_tag]["affiliation"], ""
    )

    if contributor_affiliation:
        dc_contributor["affiliation"] = \
            affiliation_to_dc(contributor_affiliation, config)

    contributor_type = maintainer.get(
        join_tags([dc_contributor_tag, "contributorType"]), "ContactPerson"
    )
    dc_contributor["@contributorType"] = value_to_datacite_cv(
        contributor_type, "contributorType"
    )

    return dc_contributor


def affiliation_to_dc(affiliation, config):
    """Returns affiliation in DataCite "affiliation" tag format.
       Uses config to map commonly used affiliations in EnviDat packages
       (i.e. "WSL", "SLF") with long names of instiutions
       and ROR identifiers when available.
    """

    # Get key from config that corresponds to affiliation
    aff_keys = {
        "WSL": "wsl",
        "Swiss Federal Institute for Forest, Snow and Landscape Research WSL": "wsl",
        "WSL Swiss Federal Research Institute, Birmensdorf, Switzerland": "wsl",
        "SLF": "slf",
        "WSL Institute for Snow and Avalanche Research SLF, Davos Dorf, Switzerland":
            "slf",
        "WSL Institute for Snow and Avalanche Research SLF": "slf",
        "ETH": "eth",
        "ETHZ": "eth",
        "UZH": "uzh",
        "University of Zurich": "uzh",
        "University of Zürich": "uzh",
        "EPFL": "epfl",
        "EPFL, Lausanne Swiss Federal Institute of Technology, Lausanne and Sion":
            "epfl",
        "PSI": "psi",
        "PSI, Paul Scherrer Institute, Villigen": "psi",
        "IAP": "iap",
        "TROPOS": "tropos",
        "UNIL": "unil"
    }

    # Get affiliation config
    aff_config = config["affiliation"]

    # Strip whitespace from affiliation
    aff = affiliation.strip()

    # Return org dictionary if it exists in config
    aff_key = aff_keys.get(aff, "")
    org = aff_config.get(aff_key, {})
    if org:
        return org
    # Else return only affiliation
    return {"#text": aff}


def get_dc_research_group(organization_title):
    """Returns organization title in DataCite "contributor" format with a
    contributorType of "ResearchGroup" """

    dc_contributor = collections.OrderedDict()

    dc_contributor["@contributorType"] = "ResearchGroup"

    dc_contributor["contributorName"] = {
        "#text": organization_title.strip(),
        "@nameType": "Organizational"
    }

    return dc_contributor


def get_dc_related_identifiers(related_identifiers, resources):
    """Return related datasets, related publications and URLs from resources in
    DataCite "relatedIdentifiers" tag format"""

    dc_related_identifiers = collections.OrderedDict()
    dc_related_identifiers["relatedIdentifier"] = []

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
                dora_start_index = word.find(dora_str)
                dora_pid = word[(dora_start_index + len(dora_str)):]

                # Remove any characters that may exist after DORA PID
                dora_end_index = dora_pid.find('/')
                dora_pid = dora_pid[:dora_end_index]

                # Call DORA API and get DOI if it listed in citation
                doi_dora = get_dora_doi(dora_pid)
                if doi_dora:
                    doi = doi_dora

            if doi and "/" in doi and doi not in related_ids:
                related_ids.append(doi)
                dc_related_identifiers["relatedIdentifier"] += [
                    {
                        "#text": doi,
                        "@relatedIdentifierType": "DOI",
                        "@relationType": "IsSupplementTo",
                    }
                ]
                continue

            # Apply URL validator to find other URLs (that are not DOIs)
            is_url = validators.url(word)

            if all([is_url, word not in related_ids, "doi" not in word]):
                related_ids.append(word)

                # EnviDat datasets are assigned a relationType of "Cites"
                if word.startswith(
                        (
                                "https://envidat.ch/#/metadata/",
                                "https://envidat.ch/dataset/")
                ):
                    dc_related_identifiers["relatedIdentifier"] += [
                        {
                            "#text": word,
                            "@relatedIdentifierType": "URL",
                            "@relationType": "Cites",
                        }
                    ]
                else:
                    # All other URLs are assigned a relationType of "IsSupplementTo"
                    dc_related_identifiers["relatedIdentifier"] += [
                        {
                            "#text": word,
                            "@relatedIdentifierType": "URL",
                            "@relationType": "IsSupplementTo",
                        }
                    ]

    # Add URLs from resources
    for resource in resources:
        resource_url = resource.get("url", "")
        if resource_url:
            dc_related_identifiers["relatedIdentifier"] += [
                {
                    "#text": resource_url,
                    "@relatedIdentifierType": "URL",
                    "@relationType": "IsRequiredBy",
                }
            ]

    return dc_related_identifiers


def get_dc_formats(resources):
    """Returns resources formats in DataCite "formats" tag format"""
    dc_formats = []

    for resource in resources:

        default_format = resource.get("mimetype", resource.get("mimetype_inner", ""))
        resource_format = resource.get("format", "")

        if not resource_format:
            resource_format = default_format

        if resource_format:
            dc_format = {"#text": resource_format}
            dc_formats += [dc_format]

    return dc_formats


def get_dc_descriptions(notes, dc_description_type_tag, dc_xml_lang_tag):
    """Returns notes in DataCite "descriptions" tag format"""
    dc_descriptions = []

    if notes:
        description_text = (
            notes.replace("\r", "")
                .replace(">", "-")
                .replace("<", "-")
                .replace("__", "")
                .replace("#", "")
                .replace("\n\n", "\n")
                .replace("\n\n", "\n")
        )

        datacite_description = {
            "#text": description_text.strip(),
            f"@{dc_description_type_tag}": "Abstract",
            f"@{dc_xml_lang_tag}": "en-us",
        }

        dc_descriptions += [datacite_description]

    return dc_descriptions


def get_dc_geolocations(spatial: dict):
    """Returns spatial information in DataCite "geoLocations" format"""

    dc_geolocations = []

    if spatial.get("type", "").lower() == "polygon":
        dc_geolocation = collections.OrderedDict()
        dc_gelocation_polygon_tag = "geoLocationPolygon"
        dc_geolocation[dc_gelocation_polygon_tag] = {"polygonPoint": []}

        for coordinates_pair in spatial.get("coordinates", "[[]]")[0]:
            geolocation_point = collections.OrderedDict()
            geolocation_point["pointLongitude"] = coordinates_pair[0]
            geolocation_point["pointLatitude"] = coordinates_pair[1]
            dc_geolocation[dc_gelocation_polygon_tag]["polygonPoint"] += [
                geolocation_point]

        dc_geolocations += [dc_geolocation]

    else:
        dc_geolocation_point_tag = "geoLocationPoint"

        if spatial.get("type", "").lower() == "multipoint":

            for coordinates_pair in spatial.get("coordinates", "[]"):
                dc_geolocation = collections.OrderedDict()
                dc_geolocation[dc_geolocation_point_tag] = collections.OrderedDict()
                dc_geolocation[dc_geolocation_point_tag]["pointLongitude"] = \
                    coordinates_pair[0]
                dc_geolocation[dc_geolocation_point_tag]["pointLatitude"] = \
                    coordinates_pair[1]
                dc_geolocations += [dc_geolocation]

        else:
            dc_geolocation = collections.OrderedDict()
            dc_geolocation[dc_geolocation_point_tag] = collections.OrderedDict()

            coordinates = flatten(spatial.get("coordinates", "[]"), reverse=True)
            dc_geolocation[dc_geolocation_point_tag]["pointLongitude"] = coordinates[1]
            dc_geolocation[dc_geolocation_point_tag]["pointLatitude"] = coordinates[0]
            dc_geolocations += [dc_geolocation]

    return dc_geolocations


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

    # Replace literal asterisk "\*" with empty string ""
    dora_pid = re.sub("\*", "", dora_pid)

    # Assemble url used to call DORA API
    dora_url = f"{host}{path}/{dora_pid}"

    try:
        data = get_url(dora_url).json()

        if data:
            citation = data[dora_pid]["citation"]["WSL"]

            for word in citation.split(" "):
                # Return DOI if it exists
                doi = get_doi(word)
                if doi:
                    return doi

            # If DOI not found then return None
            return None

        return None

    except Exception as e:
        log.error(f"ERROR: Failed to retrieve'{dora_url}' and extract DOI")
        log.error(e)
        return None

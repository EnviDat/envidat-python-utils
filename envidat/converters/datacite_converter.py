"""DataCite for linking metadata to DOIs."""

import collections
import json
from json import JSONDecodeError
from logging import getLogger

from xmltodict import unparse

log = getLogger(__name__)

FIELD_NAME = "field_name"


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
        converted_package = datacite_convert_dataset(metadata_record, name_doi_map)
        return unparse(converted_package, pretty=True)  # Convert OrderedDict to XML
    except ValueError as e:
        log.error(e)
        log.error("Cannot convert package to DataCite format.")
        raise ValueError("Failed to convert package to DataCite format.")


def datacite_convert_dataset(dataset: dict, name_doi_map: dict):
    """Create the DataCite XML from API dictionary."""
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

    # Identifier*
    datacite_identifier_tag = "identifier"
    doi = dataset.get("doi", "")
    datacite["resource"][datacite_identifier_tag] = {
        "#text": doi.strip(),
        "@identifierType": "DOI",
    }

    # Creators
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
    related_datasets = dataset.get("related_datasets", "")
    related_datasets_base_url = "https://www.envidat.ch/#/metadata/"
    if related_datasets:

        datacite_related_urls = collections.OrderedDict()
        datacite_related_urls["relatedIdentifier"] = []

        for line in related_datasets.split("\n"):

            if line.strip().startswith("*"):
                line_contents = line.replace("*", "").strip().lower().split(" ")[0]
                related_url = None

                if line_contents in name_doi_map:
                    related_url = f"{related_datasets_base_url}{line_contents}"

                elif len(line_contents) > 0 and line_contents in name_doi_map.values():
                    related_url = f"{related_datasets_base_url}{line_contents}"

                elif line_contents.startswith("https://") or line_contents.startswith(
                    "http://"
                ):
                    related_url = line_contents

                if related_url:
                    datacite_related_urls["relatedIdentifier"] += [
                        {
                            "#text": related_url,
                            "@relatedIdentifierType": "URL",
                            "@relationType": "Cites",
                        }
                    ]

        # NOTE: Investigate including commented out block below to find
        # all URLs in 'related_datasets' key:
        # regex = (
        #     'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
        #     '[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        # )
        # urls = re.findall(regex, related_datasets)
        #
        # for url in urls:
        #     datacite_related_urls['relatedIdentifier'] += [
        #         {
        #             '#text': url,
        #             '@relatedIdentifierType': 'URL',
        #             '@relationType': 'Cites'
        #         }
        #     ]

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


def map_fields(schema: dict, format_name: str) -> dict:
    """Map fields into correct formatting."""
    fields_map = {}
    for field in schema:
        format_field = ""
        if field.get(format_name, False):
            format_field = field[format_name]
            fields_map[format_field] = {FIELD_NAME: field[FIELD_NAME], "subfields": {}}
        for subfield in field.get("subfields", []):
            if subfield.get(format_name, False):
                format_subfield = subfield[format_name]
                if format_field:
                    if not fields_map[format_field]["subfields"].get(
                        format_subfield, False
                    ):
                        fields_map[format_field]["subfields"][format_subfield] = {
                            FIELD_NAME: subfield[FIELD_NAME]
                        }
                    else:
                        value = fields_map[format_field]["subfields"][format_subfield][
                            FIELD_NAME
                        ]
                        if isinstance(value, list):
                            fields_map[format_field]["subfields"][format_subfield] = {
                                FIELD_NAME: value + [subfield[FIELD_NAME]]
                            }
                        else:
                            fields_map[format_field]["subfields"][format_subfield] = {
                                FIELD_NAME: [value, subfield[FIELD_NAME]]
                            }
                else:
                    fields_map[format_subfield] = {
                        FIELD_NAME: field[FIELD_NAME] + "." + subfield[FIELD_NAME]
                    }
    return fields_map

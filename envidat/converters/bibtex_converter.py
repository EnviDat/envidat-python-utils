import json

from envidat.api.v1 import get_package, get_protocol_and_domain

from logging import getLogger

log = getLogger(__name__)


def convert_bibtex(package_json: str) -> str:
    """Returns string in BibTex format.

    Note: Converter is only valid for the metadata schema for EnviDat.

    Args:
        package_json (str): Individual EnviDat metadata entry record in JSON format.

    Returns:
        str: string in BibTeX format

    """
    try:
        package_dict = json.loads(package_json)  # Convert package JSON to dictionary
        converted_package = bibtex_convert_dataset(package_dict)  # Convert package to RIS format
        return converted_package
    except AttributeError as e:
        log.error(e)
        log.error("Cannot convert package to BibTeX format.")
        raise AttributeError("Failed to convert package to BibTeX format.")


def bibtex_convert_dataset(dataset_dict: dict) -> str:

    # name as identifier (plus year later)
    name = dataset_dict['name']
    converted_package = u"@misc { " + name

    # year (add to name) and journal
    publication = json.loads(dataset_dict.get('publication', '{}'))
    publication_year = publication["publication_year"]

    converted_package += u'-{0}'.format(publication_year)
    converted_package += u',\n\t year = "{0}"'.format(publication_year)
    publisher = publication["publisher"]
    converted_package += u',\n\t publisher = "{0}"'.format(publisher)

    # title
    title = dataset_dict['title']
    converted_package += u',\n\t title = "' + title + u'"'

    # author
    authors = json.loads(dataset_dict.get('author', '[]'))
    author_names = []
    for author in authors:
        author_name = ""
        if author.get('given_name'):
            author_name += author['given_name'].strip() + ' '
        author_names += [author_name + author['name']]
    bibtex_author = u' and '.join(author_names)
    converted_package += u',\n\t author = "{0}"'.format(bibtex_author)

    # DOI
    doi = dataset_dict.get('doi', '').strip()
    if doi:
        converted_package += u',\n\t DOI = "http://dx.doi.org/{0}"'.format(doi)

    # url
    protocol, host = get_protocol_and_domain()
    package_name = dataset_dict.get('name', '')
    url = f'{protocol}://{host}/dataset/{package_name}'
    converted_package += u',\n\t url = "' + url + '"'

    # close bracket
    converted_package += "\n\t}"

    return converted_package

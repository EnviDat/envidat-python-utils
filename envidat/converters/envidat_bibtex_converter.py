import json

from envidat.api.v1 import get_package, get_protocol_and_domain

from logging import getLogger

log = getLogger(__name__)


# TODO document class and functions with strings compatible with auto generated documentation


# This converter is only valid for the metadata schema for EnviDat
class BibtexConverter:

    def convert(self, package_name: str):
        # Try to convert pacakage dictionary to format compatible with BibTeX standard format
        try:
            package = get_package(package_name)  # Get package dictionary from API
            converted_package = self._bibtex_convert_dataset(package)  # Convert package to RIS format
            return converted_package
        except AttributeError as e:
            log.error(e)
            log.error("Cannot convert package to BibTeX format.")
            raise AttributeError("Failed to convert package to BibTeX format.")

    @staticmethod
    def _bibtex_convert_dataset(dataset_dict: dict):

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

import json
from logging import getLogger

from envidat.api.v1 import get_package, get_protocol_and_domain

log = getLogger(__name__)


# TODO document class and functions with strings compatible with auto generated documentation


# This converter is only valid for the metadata schema for EnviDat
class RisConverter:

    def convert(self, package_name: str):
        # Try to convert pacakage dictionary to format compatible with RIS standard format
        try:
            package = get_package(package_name)  # Get package dictionary from API
            converted_package = self._ris_convert_dataset(package)  # Convert package to RIS format
            return converted_package
        except AttributeError as e:
            log.error(e)
            log.error("Cannot convert package to RIS format.")
            raise AttributeError("Failed to convert package to RIS format.")

    def _ris_convert_dataset(self, dataset_dict: dict):

        ris_list = []

        #   TY  - DATA
        ris_list += [u"TY  - DATA"]

        #   T1  - Title
        title = dataset_dict['title']
        ris_list += [u"T1  - " + title]

        #   AU  - Authors
        authors = json.loads(dataset_dict.get('author', '[]'))
        for author in authors:
            author_name = ""
            if author.get('given_name'):
                author_name += author['given_name'].strip() + ' '
            author_name += author['name'].strip()
            ris_list += [u"AU  - " + author_name]

        #   DO  - DOI
        doi = dataset_dict.get('doi', '').strip()
        if doi:
            ris_list += [u"DO  - " + doi]

        #   UR  - dataset url as information
        protocol, host = get_protocol_and_domain()
        package_name = dataset_dict.get('name', '')
        package_url = f'{protocol}://{host}/dataset/{package_name}'
        ris_list += [u"UR  - " + package_url]

        #   KW  - keywords
        keywords = self._get_keywords(dataset_dict)
        for keyword in keywords:
            ris_list += [u"KW  - " + keyword]

        #   PY  - publication year
        publication = json.loads(dataset_dict.get('publication', '{}'))
        publication_year = publication["publication_year"]
        ris_list += [u"PY  - " + publication_year]

        #   PB  - Publisher
        publisher = publication["publisher"]
        ris_list += [u"PB  - " + publisher]

        #   LA  - en
        language = dataset_dict.get('language', 'en').strip()
        if len(language) <= 0:
            language = 'en'
        ris_list += [u"LA  - " + language]

        #   ER  -
        ris_list += [u"ER  - "]

        return "\n".join(ris_list)

    # Extract keywords from tags
    @staticmethod
    def _get_keywords(data_dict: dict):
        keywords = []
        for tag in data_dict.get('tags', []):
            name = tag.get('display_name', '').upper()
            keywords += [name]
        return keywords

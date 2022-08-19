import json
from logging import getLogger

from envidat.api.v1 import get_package, get_protocol_and_domain

# import ckan.lib.helpers as helpers
# import ckan.plugins.toolkit as toolkit
# from ckanext.package_converter.model.converter import BaseConverter
# from ckanext.package_converter.model.metadata_format import MetadataFormats
# from ckanext.package_converter.model.record import Record

log = getLogger(__name__)


# TODO document class and functions with strings compatible with auto generated documentation


# This converter is only valid for the metadata schema for EnviDat
class RisConverter:

    # def __init__(self):
    #     ris_output_format = MetadataFormats().get_metadata_formats('ris')[0]
    #     BaseConverter.__init__(self, ris_output_format)

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

        # if self.can_convert(record):
        #     dataset_dict = record.get_json_dict()
        #     converted_content = self._ris_convert_dataset(dataset_dict)
        #     converted_record = Record(self.output_format, converted_content)
        #     return converted_record
        # else:
        #     raise TypeError(('Converter is not compatible with the record format {record_format}({record_version}). ' +
        #                      'Accepted format is CKAN {input_format}.').format(
        #         record_format=record.get_metadata_format().get_format_name(),
        #         record_version=record.get_metadata_format().get_version(),
        #         input_format=self.get_input_format().get_format_name()))

    # def __unicode__(self):
    #     return super(RisConverter, self).__unicode__() + u'RIS Converter '

    def _ris_convert_dataset(self, dataset_dict):

        ris_list = []

        #   TY  - DATA
        ris_list += [u"TY  - DATA"]

        #   T1  - Title
        title = dataset_dict['title']
        ris_list += [u"T1  - " + title]

        #   AU  - Authors
        authors = json.loads(dataset_dict.get('author', '[]'))
        # author_names = []
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
        # protocol, host = helpers.get_site_protocol_and_host()
        # url = protocol + '://' + host + toolkit.url_for(controller='dataset', action='read',
        #                                                 id=dataset_dict.get('name', ''))
        # ris_list += [u"UR  - " + url]
        protocol, host = get_protocol_and_domain()
        package_name = dataset_dict.get('name', '')
        package_url = f'{protocol}://{host}/dataset/{package_name}'
        ris_list += [u"UR  - " + package_url]

        #   KW  - keywords (type default to theme)
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
    def _get_keywords(data_dict):
        keywords = []
        for tag in data_dict.get('tags', []):
            name = tag.get('display_name', '').upper()
            keywords += [name]
        return keywords


# ================== TESTING
converter = RisConverter()
# result = converter.convert('envidat-lwf-45')
result = converter.convert('distribution-maps-of-permanent-grassland-habitats-for-switzerland')
print(result)

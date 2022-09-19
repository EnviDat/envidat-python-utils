"""Get CKAN API package converters endpoints."""

import os

import logging
log = logging.getLogger(__name__)


def get_ris_ckan_endpoint(
        package: dict, host: str = 'https://www.envidat.ch'
) -> str:

    if "API_HOST" in os.environ:
        log.debug("Getting API host from environment variable.")
        host = os.getenv("API_HOST")

    package_name = package.get('name', '')
    if package_name:
        return f'{host}/dataset/{package_name}/export/ris.ris'
    else:
        package_id = package.get('id', '')
        if package_id:
            return f'{host}/dataset/{package_id}/export/ris.ris'
        else:
            raise ValueError('Failed to get RIS CKAN endpoint string.')

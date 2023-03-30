import json

import requests
from dotenv import dotenv_values
from envidat.email.constants import PublishAction, PublishSubject, PublishTemplateName

from logging import getLogger
log = getLogger(__name__)


# TODO improve exception handling with more specific exceptions
# TODO write docstring
def get_user_name_email(user_id: str):

    # Load config from environment vairables
    config = dotenv_values(".env")

    # Extract environment variables from config needed to call CKAN
    try:
        API_HOST = config["API_HOST"]
        API_USER_SHOW = config["API_USER_SHOW"]
        API_KEY = config["API_KEY"]
    except KeyError as e:
        log.error(f'KeyError: {e} does not exist in config')
        return None, None
    except AttributeError as e:
        log.error(e)
        return None, None

    # Extract and return user's name and email from user account data
    # returned from CKAN API call
    try:
        # Request user's account from CKAN
        api_url = f"{API_HOST}{API_USER_SHOW}{user_id}"
        headers = {"Authorization": API_KEY}
        response = requests.get(api_url, headers=headers)

        # Handle unexpected response status_code
        # Expected successful response status_code: 200
        if response.status_code != 200:
            log.error(
                f"ERROR: Call to CKAN returned unexpected response status_code "
                f"{response.status_code}")
            return None, None

        # Return user's name and email address
        if response:
            data = response.json()
            user_account = data["result"]
            user_name = user_account["fullname"].strip()
            user_email = user_account["email"]
            return user_name, user_email

    except ConnectionError as e:
        log.error(e)
        return None, None

    except Exception as e:
        log.error(e)
        return None, None


# TODO implement templates for all publish_action cases
# TODO write docstring
# Get subject and template that corresponds to publication_action
def get_publish_email_subject_template(publish_action):

    match publish_action:

        case PublishAction.REQUEST:
            subject = PublishSubject.REQUEST.value
            template_name = PublishTemplateName.REQUEST.value

        case PublishAction.APPROVE:
            subject = PublishSubject.APPROVE.value
            template_name = PublishTemplateName.REQUEST.value

        case PublishAction.DENY:
            subject = PublishSubject.DENY.value
            template_name = PublishTemplateName.REQUEST.value

        case PublishAction.FINISH:
            subject = PublishSubject.FINISH.value
            template_name = PublishTemplateName.REQUEST.value

        # TODO handle default case
        case _:
            # TODO log error
            return None, None

    return subject, template_name

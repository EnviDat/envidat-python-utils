from envidat.api.v1 import get_envidat_record
from envidat.doi.datacite_publisher import publish_datacite
from fastapi import APIRouter, Response
from fastapi.templating import Jinja2Templates
from fastapi_mail import MessageType
from pydantic import EmailStr
from envidat.email.constants import PublishAction, PublishSubject, PublishTemplateName

import logging

from envidat.email.send_email import send_email_async

log = logging.getLogger(__name__)


router = APIRouter(
    prefix="/publish",
    tags=["publish"]
)


# TODO implement authentication, likely with JWT tokens
# TODO check if AttributeError is best way to handle unknown errors
# TODO check if 500 is best default error status code
# TODO investigate how to add schema to API documentation on /docs
# TODO write doc string
# TODO test triggering all errors
@router.get("/datacite", tags=["publish"])
def publish_record_to_datacite(name: str, response: Response):

    # Get EnviDat record from CKAN API call
    try:
        record = get_envidat_record(name)

        # Handle HTTP errors from CKAN API call (default status_code is 500)
        status_code = record.get("status_code", 500)
        if status_code != 200:
            response.status_code = status_code
            return {"error": record.get("result",
                                        "Failed to extract record as JSON from CKAN "
                                        "API, check logs")}
    except AttributeError as e:
        log.error(e)
        response.status_code = 500
        return {"error": "Failed to extract record as JSON from CKAN API, check logs"}

    # Publish package to DataCite and return DOI
    try:
        # Extract package from record result
        package = record.get("result")

        # Publish package to DataCite
        if package:
            dc_response = publish_datacite(package)
        else:
            response.status_code = 500
            return {"error": "Failed to extract 'result' from record"}

        # Assign response status_code (default status_code is 500)
        # Expected successful response status_code: 201
        dc_status_code = dc_response.get("status_code", 500)
        response.status_code = dc_status_code

        # Handle HTTP errors from publishing to DataCite
        if dc_status_code != 201:
            return {"error": dc_response.get("result", "Internal Server Error")}

        # TODO implement notification email
        # Else send notification email and return published DOI
        return {"doi": dc_response.get("result")}

    except AttributeError as e:
        log.error(e)
        response.status_code = 500
        return {
            "error": "Failed to publish EnviDat record to DataCite, check logs"}


# TODO rename function, handle specific use cases and general ones
# TODO make a email sender function that uses background tasks
# TODO determine template variables based off of template type
# TODO try to find correspoding template and match (otherwise send error),
#  then send email
# TODO find recipient email by calling CKAN and using user ID
# TODO check if templates should be HTML or plain text
# TODO add user's organization admins to recipients by calling CKAN and using user's
#  organizations' id
# TODO implement try/exception error handling
@router.get('/email/{publish_action}')
async def send_email_publish_async(publish_action: PublishAction,
                                   recipient: EmailStr,
                                   package_name: str,
                                   admin_email: str = 'envidat@wsl.ch',
                                   subtype: MessageType = MessageType.plain):
    # Assign recipients
    recipients = [recipient, admin_email]

    # TODO extract get template and get subject to separate helper functions
    # TODO review formatting of subject (i.e. including colon)
    # TODO implement templates for all publish_action cases
    # Get subject and template that corresponds to publication_action
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
            return

    # TODO check if package_name should be validated,
    #  (hyphens between names and no white space)
    subject = f"{subject}: {package_name}"

    # Use template to get message body
    # Load Jinga2 templates
    templates = Jinja2Templates(directory="templates")

    # template = templates.get_template("email.html")
    template = templates.get_template(str(template_name))

    template_variables = {
        "title": "test",
        "name": "Rebecca"
    }

    body = template.render(**template_variables)

    # TODO include package name in subject
    await send_email_async(subject,
                           recipients,
                           body,
                           subtype)

    return 'Success'

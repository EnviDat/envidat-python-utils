from enum import Enum

from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi_mail import MessageType
from pydantic import EmailStr
from fastapi.templating import Jinja2Templates

from envidat.email.constants import PublishAction, PublishSubject, PublishTemplateName
from envidat.email.send_email import send_email_async, send_email_background, \
    send_email_background_test
from routers import router_publish

# Declare app instance of FastAPI()
app = FastAPI()

# Add router_publish to app
app.include_router(router_publish.router)

# Load Jinga2 templates
templates = Jinja2Templates(directory="templates")


@app.get("/", tags=["home"])
def home():
    html_content = """
    <html>
        <head>
            <title>EnviDat API</title>
        </head>
        <body>
            <h1>Welcome to the wonderfully weird world of whales!</h1>
            <h3>Need help? Check out the docs at "/docs",
               for example <a href="http://127.0.0.1:8000/docs" target="_blank">
               http://127.0.0.1:8000/docs</a><h3>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


# TODO test endpoint
@app.get('/send-email/backgroundtasks')
def send_email_backgroundtasks(background_tasks: BackgroundTasks):
    send_email_background_test(background_tasks, 'Hello World', 'test@test.com',
                               # {'title': 'Hello World', 'name': 'Whaley'}
                               )

    # return 'Success'


# TODO test endpoint
# @app.get('/send-email/asynchronous')
# async def send_email_asynchronous(recipient: EmailStr):
#     # TODO include package name in email title
#     await send_email_async(recipient,
#                            # {'title': 'Hello World', 'name': 'Whaley'}
#                            )
#
#     return 'Success'


# TODO move email function(s) to a router file
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
@app.get('/send-email/publish/{publish_action}')
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

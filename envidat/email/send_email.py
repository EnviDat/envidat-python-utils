import json
import ssl
from typing import Dict, Any
from fastapi.templating import Jinja2Templates

from fastapi import BackgroundTasks, Path, Request

# TODO remove fastapi_mail
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from dotenv import dotenv_values
import smtplib

# TODO review setup of logging
from logging import getLogger

from jinja2 import Template, Environment, PackageLoader, select_autoescape
from pydantic import EmailStr

log = getLogger(__name__)

# TODO remove unused functions
# TODO remove unused environment variables


# Load Jinga2 templates
# templates = Jinja2Templates(directory="templates")


# TODO write docstring
# Return ConnectionConfig class extracted from mail environment variables
def get_email_config():
    # Load config from environment vairables
    config = dotenv_values(".env")

    # Extract environment variables from config needed to send emails
    try:
        # TODO review email config
        connection_config = ConnectionConfig(
            MAIL_USERNAME=config["MAIL_USERNAME"],
            MAIL_PASSWORD=config["MAIL_PASSWORD"],
            MAIL_FROM=config["MAIL_FROM"],
            MAIL_PORT=config["MAIL_PORT"],  # TODO review port
            MAIL_SERVER=config["MAIL_SERVER"],
            MAIL_FROM_NAME=config["MAIL_FROM_NAME"],
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            # TEMPLATE_FOLDER='envidat/email/templates'
            # TEMPATE_FOLDER='templates'
        )
        return connection_config

    except KeyError as e:
        log.error(f'KeyError: {e} does not exist in config')
        return None

    except AttributeError as e:
        log.error(e)
        return None


# TODO remove message
message_test = f"""\
Subject: Publication Finished
To: test@test.com
From: test@test.com

This is a test e-mail message. WHALEY"""


# TODO remove function
# TODO write docstring
# TODO implement route with background tests
# TODO rename function
# TODO create template for emails, extract variables needed into a function and
#  template that writes message
# TODO refactor so that None is returned in case of error,
#  if success return value or message
def send_email_background():
    # Load config from environment vairables
    config = dotenv_values(".env")

    # Extract environment variables from config needed to send emails
    try:
        port = int(config["MAIL_PORT"])
        mail_server = config["MAIL_SERVER"]
        pswd = config["MAIL_PASSWORD"]
        username = config["MAIL_USERNAME"]
    except KeyError as e:
        log.error(f'KeyError: {e} does not exist in config')
        return None
    except AttributeError as e:
        log.error(e)
        return None

    sender = "test@test.com"
    receiver = "test@test.com"

    # Encrypt message using TLS
    try:
        # Start SMPT server
        with smtplib.SMTP(mail_server, port) as server:

            # Secure the connection
            context = ssl.create_default_context()
            server.starttls(context=context)

            # Login and send email
            server.login(username, pswd)
            server.sendmail(sender, receiver, message_test)
            server.quit()

            # TODO return success message or other success value
            # sucessfully sending mail (not necessarily recieved)
            # will result in empty dictionary {}
            # result = server.sendmail(sender, receiver, message)
            # print(result)

    except smtplib.SMTPException as e:
        log.error(e)
        return None

    except AttributeError as e:
        log.error(e)
        return None


# TODO test function
# TODO refactor function to use updated config
def send_email_background_test(background_tasks: BackgroundTasks,
                               subject: str, email_to: str,
                               # body: dict
                               ):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        # body=body,
        body="""
<p>Thanks for using Fastapi-mail</p>
""",
        subtype='html',
    )

    # Assign email config
    conf = get_email_config()
    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message,
                              # template_name='email.html'
                              )


# # TODO test function
# # TODO refactor function to use updated config
# # async def send_email_async(recipient: str):
# async def send_email_async(recipient: str, body: dict):
#
#     # Load
#
#     # Assign message object
#     message = MessageSchema(
#
#         # TODO review default subject, should it include package name
#         subject='Publication Finished',
#
#         # TODO review if EnviDat should be also be default recipient
#         recipients=[recipient, 'envidat@wsl.ch'],
#
#         # body=body,
#         # body="""
#         # <p>Have a nice day from EnviDat</p>
#         # """,
#         # template_body=json.dumps({'title': 'Hello World', 'name': 'Whaley'}),
#
#         tempate_body=body,
#
#         subtype=MessageType.html
#         # subtypte='html'
#     )
#
#     # Assign email config
#     conf = get_email_config()
#     fm = FastMail(conf)
#
#     print(conf)
#
#     # Send email
#     # await fm.send_message(message)
#     await fm.send_message(message, template_name='envidat/email/templates/email.html')
#     # await fm.send_message(message, template_name='email.html')
#     # await fm.send_message(message, template_name=None)
#     # template_name='email.html'
#     # )


# TODO test function
# TODO refactor function to use updated config
# async def send_email_async(recipient: str):
async def send_email_async(recipients: list[EmailStr],
                           # template: Template
                           # body: dict
                           ):

    # TODO determine template variables based off of template type
    # TODO try to find correspoding template and match (otherwise send error),
    #  then send email
    pass

    # email_content = templates.TemplateResponse("email.html", {'request': Request,
    #                                                           'title': 'Hello World',
    #                                                           'name': 'Whaley'})
    #
    # return email_content

    # env = Environment(loader=PackageLoader('email', 'templates'),
    #                   autoescape=select_autoescape(['html', 'xml'])
    #                   )
    #
    # template = env.get_template('email.html')

    # # Assign message object
    # message = MessageSchema(
    #
    #     # TODO review default subject, should it include package name
    #     subject='Publication Finished',
    #
    #
    #     recipients=recipients,
    #
    #     # body=body,
    #     # body="""
    #     # <p>Have a nice day from EnviDat</p>
    #     # """,
    #     # template_body=json.dumps({'title': 'Hello World', 'name': 'Whaley'}),
    #
    #     tempate_body=body,
    #
    #     subtype=MessageType.html
    #     # subtypte='html'
    # )
    #
    # # Assign email config
    # conf = get_email_config()
    # fm = FastMail(conf)
    #
    # print(conf)
    #
    # # Send email
    # # await fm.send_message(message)
    # await fm.send_message(message, template_name='envidat/email/templates/email.html')
    # # await fm.send_message(message, template_name='email.html')
    # # await fm.send_message(message, template_name=None)
    # # template_name='email.html'
    # # )

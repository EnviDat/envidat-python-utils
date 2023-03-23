import ssl

from fastapi import BackgroundTasks

# TODO remove fastapi_mail
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from dotenv import dotenv_values
import smtplib

# TODO review setup of logging
from logging import getLogger

log = getLogger(__name__)


# TODO remove unused functions
# TODO remove unused environment variables


# TODO write docstring
# Return ConnectionConfig class extracted from mail environment variables
def get_email_config():
    # Load config from environment vairables
    config = dotenv_values(".env")

    # Extract environment variables from config needed to send emails
    try:
        # TODO review email config
        connection_config = ConnectionConfig(
            # TODO test without full address
            MAIL_USERNAME=config["MAIL_USERNAME"],
            MAIL_PASSWORD=config["MAIL_PASSWORD"],
            MAIL_FROM=config["MAIL_FROM"],
            MAIL_PORT=config["MAIL_PORT"],  # TODO review port
            MAIL_SERVER=config["MAIL_SERVER"],
            # TODO include package name in email title
            MAIL_FROM_NAME=config["MAIL_FROM_NAME"],
            MAIL_STARTTLS=bool(config["MAIL_STARTTLS"]),
            MAIL_SSL_TLS=bool(config["MAIL_SSL_TLS"]),
            USE_CREDENTIALS=bool(config["USE_CREDENTIALS"]),
            VALIDATE_CERTS=bool(config["VALIDATE_CERTS"]),
            TEMPLATE_FOLDER="envidat/email/templates"
        )
        return connection_config

    except KeyError as e:
        log.error(f'KeyError: {e} does not exist in config')
        return None

    except AttributeError as e:
        log.error(e)
        return None


message = f"""\
Subject: Publication Finished
To: test@test.com
From: test@test.com

This is a test e-mail message. WHALEY"""


# TODO write docstring
# TODO implement route with background tests
# TODO rename function
# TODO create template for emails, extract variables needed into a function and
#  template that writes message
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

    # Encrypt message using TLS, login into server and send email
    try:
        # Create SMPT instance
        server = smtplib.SMTP(mail_server, port)

        # Secure the connection
        context = ssl.create_default_context()
        server.starttls(context=context)

        # Login and send email
        server.login(username, pswd)
        server.sendmail(sender, receiver, message)
        server.quit()

    except smtplib.SMTPException as e:
        log.error(e)
    except AttributeError as e:
        log.error(e)


# TODO test function
# TODO remove
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

    background_tasks.add_task(fm.send_message, message, template_name='email.html')


# TODO test function
async def send_email_async(subject: str, email_to: str,
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

    await fm.send_message(message,
                          # template_name='email.html'
                          )

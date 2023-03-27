from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse
from pydantic import EmailStr
from fastapi.templating import Jinja2Templates

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


# TODO rename function, handle specific use cases and gneral ones
# TODO make a email sender function that uses background tasks
@app.get('/send-email/asynchronous')
async def send_email_asynchronous(recipient: EmailStr):
    # TODO review if EnviDat should be also be default recipient
    recipients = [recipient, 'envidat@wsl.ch']

    template = templates.get_template("email.html")

    template_variables = {
        "title": "test",
        "name": "Rebecca"
    }

    test = template.render(**template_variables)
    return test

    # TODO include package name in email title
    # return await send_email_async(recipients,
    #                               templates.get_template('email.html'),
    # {'title': 'Hello World', 'name': 'Whaley'}
    # templates.TemplateResponse('email.html',
    #                            {'title': 'Hello World',
    #                             'name': 'Whaley'}
    #                            )
    # )

    # await send_email_async(recipients,
    #                        {'title': 'Hello World', 'name': 'Whaley'}
    #                        )
    # return 'Success'

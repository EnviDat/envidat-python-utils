from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse

from envidat.email.send_email import send_email_async, send_email_background, \
    send_email_background_test
from routers import router_publish


# Declare app instance of FastAPI()
app = FastAPI()

# Add router_publish to app
app.include_router(router_publish.router)


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
@app.get('/send-email/asynchronous')
async def send_email_asynchronous():
    # TODO include package name in email title
    await send_email_async('Publication Finished'
                           # 'test@test.ch'
                           # {'title': 'Hello World', 'name': 'Whaley'}
                           )

    return 'Success'

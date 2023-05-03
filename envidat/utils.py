"""Extra utils used internally and within EnviDat projects."""

import logging
import os
import sys
import urllib.parse
from pathlib import Path
from typing import NoReturn, Union

import requests

log = logging.getLogger(__name__)


def _debugger_is_active() -> bool:
    """Check to see if running in debug mode.

    Returns:
        bool: if a debug trace is present or not.
    """
    gettrace = getattr(sys, "gettrace", lambda: None)
    return gettrace() is not None


def load_dotenv_if_in_debug_mode(env_file: Union[Path, str]) -> NoReturn:
    """Load secret .env variables from repo for debugging.

    Args:
        env_file (Union[Path, str]): String or Path like object pointer to
            secret dot env file to read.
    """
    if not _debugger_is_active():
        return

    try:
        from dotenv import load_dotenv
    except ImportError as e:
        log.error(
            """
            Unable to import dotenv.
            Note: The logger should be invoked after reading the dotenv file
            so that the debug level is by the environment.
            """
        )
        log.error(e)
        raise ImportError from e(
            """
            Unable to import dotenv, is python-dotenv installed?
            Try installing this package using pip install envidat[dotenv].
            """
        )

    secret_env = Path(env_file)
    if not secret_env.is_file():
        log.error(
            """
            Attempted to import dotenv, but the file does not exist.
            Note: The logger should be invoked after reading the dotenv file
            so that the debug level is by the environment.
            """
        )
        raise FileNotFoundError from None(
            f"Attempted to import dotenv, but the file does not exist: {env_file}"
        )
    else:
        load_dotenv(secret_env)


def get_logger() -> logging.basicConfig:
    """Set logger parameters with log level from environment.

    Note:
        Defaults to DEBUG level, unless specified by LOG_LEVEL env var.
    """
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", default="DEBUG"),
        format=(
            "%(asctime)s.%(msecs)03d [%(levelname)s] "
            "%(name)s | %(funcName)s:%(lineno)d | %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )
    log.debug("Logger set to STDOUT.")


# TODO use this function to replace get_user_show()
#  in router_publish.send_email_publish_async()
# TODO improve exception handling with more specific exceptions
# TODO write docstring
def get_response_json(
    api_host: str,
    api_path: str,
    query: dict | None = None,
    api_key: str | None = None,
    status_code: int = 200,
) -> dict | None:
    """Get response JSON from EnviDat."""
    load_dotenv_if_in_debug_mode(".env")

    key = None
    # Extract environment variables needed to call API URL
    try:
        host = os.environ(api_host)
        path = os.environ(api_path)
        if api_key:
            key = os.environ(api_key)
    except KeyError as e:
        log.error(f"KeyError: {e} does not exist in environnment vars")
        return None
    except AttributeError as e:
        log.error(e)
        return None

    # Call API and return JSON response
    try:
        # Call API with query params if they are truthy
        if query:
            params = urllib.parse.urlencode(query)
            api_url = f"{host}{path}?{params}"
        else:
            api_url = f"{host}{path}"

        # Add headers to request if key truthy
        if key:
            headers = {"Authorization": key}
            response = requests.get(api_url, headers=headers)
        else:
            response = requests.get(api_url)

        # Handle unexpected response status_code
        # Default expected response status_code is 200
        if response.status_code != status_code:
            log.error(
                f"ERROR call to API returned unexpected response status_code: "
                f"{response.status_code}"
            )
            log.error(f"ERROR message from API: {response.json()}")
            return None

        # Return JSON response
        if response:
            return response.json()

    except ConnectionError as e:
        log.error(e)
        return None

    except Exception as e:
        log.error(e)
        return None


def get_url(url: str) -> requests.Response:
    """Get a URL with additional error handling.

    Args:
        url (str): The URL to GET.
    """
    try:
        log.debug(f"Attempting to get {url}")
        r = requests.get(url)
        r.raise_for_status()
        return r
    except requests.exceptions.ConnectionError as e:
        log.error(f"Could not connect to internet on get: {r.request.url}")
        log.error(e)
    except requests.exceptions.HTTPError as e:
        log.error(f"HTTP response error on get: {r.request.url}")
        log.error(e)
    except requests.exceptions.RequestException as e:
        log.error(f"Request error on get: {r.request.url}")
        log.error(f"Request: {e.request}")
        log.error(f"Response: {e.response}")
    except Exception as e:
        log.error(e)
        log.error(f"Unhandled exception occurred on get: {r.request.url}")

    return None


# TODO refactor this or get_url() as they have similar functionality
def get_url_response(url: str, cookie: str | None = None) -> requests.Response:
    """Get a URL with additional error handling.

    Args:
        url (str): The URL to GET.
        cookie (str | None): Cookie passed to API call in header,
                             default value is None as this argument is not always used
    """
    try:
        log.debug(f"Attempting to get {url}")

        # Call API with cookie in header if it exists
        if cookie:
            headers = {"Cookie": cookie}
            r = requests.get(url, headers=headers)
        # Else call API (without header)
        else:
            r = requests.get(url)

        # Raise HTTP error it if occured
        r.raise_for_status()
    except requests.exceptions.ConnectionError as e:
        log.error(f"Could not connect to internet on get: {r.request.url}")
        log.error(e)
    except requests.exceptions.HTTPError:
        log.error(f"HTTP response error on get: {r.request.url}")
    except requests.exceptions.RequestException as e:
        log.error(f"Request error on get: {r.request.url}")
        log.error(f"Request: {e.request}")
        log.error(f"Response: {e.response}")
    except Exception as e:
        log.error(e)
        log.error(f"Unhandled exception occurred on get: {r.request.url}")

    return r

#

### load_dotenv_if_in_debug_mode

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/utils.py/#L40)

```python
.load_dotenv_if_in_debug_mode(
   env_file: Union[Path, str] = os.getenv('DOTENV_PATH', default = '.env'),
   ignore_docker_check: bool = False
)
```

---

Load secret .env variables from repo for debugging.

**Args**

- **env_file** (Union[Path, str]) : String or Path like object pointer to
  secret dot env file to read.
- **ignore_docker_check** (bool) : Skip checking if running via Docker.

---

### get_logger

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/utils.py/#L90)

```python
.get_logger()
```

---

Set logger parameters with log level from environment.

**Note**

Defaults to DEBUG level, unless specified by LOG_LEVEL env var.

---

### get_url

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/utils.py/#L175)

```python
.get_url(
   url: str
)
```

---

Get a URL with additional error handling.

**Args**

- **url** (str) : The URL to GET.

---

### \_debugger_is_active

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/utils.py/#L15)

```python
._debugger_is_active()
```

---

Check to see if running in debug mode.

**Returns**

- **bool** : if a debug trace is present or not.

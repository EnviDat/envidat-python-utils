#

### get_metadata_list

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/api/v1.py/#L16)

```python
.get_metadata_list(
   host: str = 'https: //www.envidat.ch', sort_result: bool = None
)
```

---

Get package/metadata list from API.

Host url as a parameter or from environment.

**Args**

- **host** (str) : API host url. Attempts to get from environment if omitted.
  Defaults to https://www.envidat.ch.
- **sort_result** (bool) : Sort result alphabetically by metadata name.
  Default to None.

**Returns**

- **list** : List of JSON formatted packages.

---

### get_protocol_and_domain

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/api/v1.py/#L56)

```python
.get_protocol_and_domain(
   protocol: str = 'https', domain: str = 'www.envidat.ch'
)
```

---

Extract protocol string and domain string from API host.

**Args**

- **protocol** (str) : API host protocol. Attempts to get from environment if omitted.
  Defaults to https
- **domain** (str) : API host domain. Attempts to get from environment if omitted.
  Defaults to www.envidat.ch

**Returns**

- **tuple** (<str: protocol>, <str: domain>) : Protocol and domain from API host.

---

### get_package

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/api/v1.py/#L79)

```python
.get_package(
   package_name: str, host: str = 'https: //www.envidat.ch',
   path: str = '/api/action/package_show?id = '
)
```

---

Get individual package (metadata entry) as dictionary from API.

**Args**

- **package_name** (str) : API package 'name' or 'id' value.
- **host** (str) : API host url. Attempts to get from environment if omitted.
  Defaults to "https://www.envidat.ch"
- **path** (str) : API host path. Attempts to get from environment if omitted.
  Defaults to "api/action/package_show?id="

**Returns**

- **dict** : Dictionary of package (metadata entry).

---

### get_metadata_json_with_resources

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/api/v1.py/#L183)

```python
.get_metadata_json_with_resources(
   host: str = 'https: //www.envidat.ch',
   path: str = '/api/3/action/current_package_list_with_resources?limit = 100000'
)
```

---

Get all current package/metadata as dictionary with associated resources from
API.

**Args**

- **host** (str) : API host url. Attempts to get from environment if omitted.
  Defaults to https://www.envidat.ch
- **path** (str) : API host path. Attempts to get from environment if omitted.
  Defaults to /api/3/action/current_package_list_with_resources?limit=100000

**Note**

Limits results to 100000, otherwise returns only 10 results.

**Returns**

- **dict** : Dictionary of packages, with nested resources.

---

### get_metadata_list_with_resources

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/api/v1.py/#L221)

```python
.get_metadata_list_with_resources(
   sort_result: bool = None
)
```

---

Get all current package/metadata as list of results with associated resources.

**Args**

- **sort_result** (bool) : Sort result alphabetically by metadata name.
  Default to None.

**Note**

Limits results to 100000, otherwise returns only 10 results.

**Returns**

- **list** : List of packages, with nested resources.

---

### get_metadata_name_doi

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/api/v1.py/#L252)

```python
.get_metadata_name_doi()
```

---

Get all current package/metadata names and DOIs as a dictionary.

**Note**

Packages that do not have DOIs are assigned a default value
of an empty string ''.

**Returns**

- **dict** : Dictionary of package information with names as keys
  and associated DOIs as values.

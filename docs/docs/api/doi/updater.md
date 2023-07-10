#

### datacite_update_all_records

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/doi/datacite_updater.py/#L29)

```python
.datacite_update_all_records()
```

---

Updates existing DOIs for all EnviDat records on DataCite.

Function converts all EnviDat records to DataCite Metadata Schema 4.4,
for documentation: https://schema.datacite.org/meta/kernel-4.4/

For documentation of DataCite API: https://support.datacite.org/docs/api

For DataCite API reference:
https://support.datacite.org/reference/introduction

For documentation of DataCite API endpoint that updates DOIs:
https://support.datacite.org/reference/put_dois-id

---

### datacite_update_records

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/doi/datacite_updater.py/#L73)

```python
.datacite_update_records(
   record_names: list[str]
)
```

---

Updates existing DOIs for EnviDat records on DataCite.

ASSUMPTION: Records already exist on DataCite and should be updated.

Function converts EnviDat records to DataCite Metadata Schema 4.4, for
documentation: https://schema.datacite.org/meta/kernel-4.4/

For documentation of DataCite API: https://support.datacite.org/docs/api

For DataCite API reference:
https://support.datacite.org/reference/introduction

For documentation of DataCite API endpoint that updates DOIs:
https://support.datacite.org/reference/put_dois-id

**Args**

- **record_names** (list[str]) : List of EnviDat records names that should be
  updated. Example: ["mountland-jura", "envidat-lwf-51"]

---

### datacite_update_one_record

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/doi/datacite_updater.py/#L108)

```python
.datacite_update_one_record(
   name: str, dc_dois: list[str] = None
)
```

---

Updates existing DOI for one EnviDat record on DataCite.

ASSUMPTION: Record already exists on DataCite and should be updated.

Function converts EnviDat record to DataCite Metadata Schema 4.4, for
documentation: https://schema.datacite.org/meta/kernel-4.4/

For documentation of DataCite API: https://support.datacite.org/docs/api

For DataCite API reference:
https://support.datacite.org/reference/introduction

For documentation of DataCite API endpoint that updates DOIs:
https://support.datacite.org/reference/put_dois-id

**Args**

- **name** (str) : EnviDat records name that should be updated.

**Example**

- **dc_dois** (list[str]) : List of DOIs with a specified DOI prefix in
  DataCite. This prefix is assigned in the config to the EnviDat
  prefix in DataCite.
  This arg is used during update of
  all records in datacite_update_all_records()
  Default value is None.

**Returns**

- **None** : Returns dictionary with DataCite response data.
  If update fails then returns None.

---

### get_dc_dois

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/doi/datacite_updater.py/#L205)

```python
.get_dc_dois(
   num_records: int = 10000
)
```

---

Return a list of DOIs with a specified DOI prefix in DataCite.

"DOI_PREFIX" in config is set to prefix assigned to EnviDat in DataCite.

For DataCite API documentation of endpoint to get list of DOIs see:
https://support.datacite.org/docs/api-get-lists

**Args**

- **num_records** (int) : Number of records to retrieve from DORA API.
  Default value is 10000.

---

### get_published_record_names_with_dois

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/doi/datacite_updater.py/#L254)

```python
.get_published_record_names_with_dois()
```

---

Return EnviDat record names that have a DOI and a "publication_state"
value of "published".

Logs records that do not have a DOI or have a DOI but a
"publication_state" value of "reserved".

**Returns**

and "doi" keys. Returns None if failed to obtain list.

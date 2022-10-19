#

## Record

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L32)

```python
Record(
   input_data: Union[str, dict], convert: Literal['str', 'xml', 'iso', 'bibtex',
   'dif', 'datacite', 'ris', 'dcat-ap'] = None
)
```

---

Class manipulate an EnviDat record in various ways.

**Methods:**

### .get_content

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L96)

```python
.get_content()
```

---

Get current content of Record.

**Returns**

- **str** : Metadata record, default dict format, else converted (JSON, XML, etc).

### .validate

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L105)

```python
.validate()
```

---

Validate metadata record.

**Returns**

- **bool** : True if valid, raises error if not.

### .to_json

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L170)

```python
.to_json()
```

---

Convert content to JSON string.

**Returns**

- **str** : JSON string of metadata record.

### .to_xml

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L179)

```python
.to_xml()
```

---

Convert content to XML format.

**Returns**

- **str** : XML formatted string of metadata record.

### .to_iso

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L188)

```python
.to_iso()
```

---

Convert content to ISO format.

**Returns**

- **str** : ISO formatted string of metadata record.

### .to_ris

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L197)

```python
.to_ris()
```

---

Convert content to RIS format.

**Returns**

- **str** : RIS formatted string of metadata record.

### .to_bibtex

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L206)

```python
.to_bibtex()
```

---

Convert content to BibTeX format.

**Returns**

- **str** : BibTeX formatted string of metadata record.

### .to_dif

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L215)

```python
.to_dif()
```

---

Convert content to GCMD DIF 10.2 format.

**Returns**

- **str** : GCMD DIF 10.2 formatted string of metadata record.

### .to_datacite

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L224)

```python
.to_datacite(
   name_doi_map: dict
)
```

---

Convert content to DataCite format.

**Args**

- **name_doi_map** (dict) : Mapping of dataset name to DOI, format name:doi.

**Returns**

- **str** : DataCite formatted string of metadata record.

### .to_dcat_ap

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L236)

```python
.to_dcat_ap()
```

---

Convert content to DCAT-AP CH format.

**Returns**

- **str** : DCAT-AP CH formatted string of metadata record.

---

### get_all_metadata_record_list

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L246)

```python
.get_all_metadata_record_list(
   convert: Literal['str', 'xml', 'iso', 'bibtex', 'dif', 'datacite', 'ris',
   'dcat-ap'] = None, content_only: bool = False
)
```

---

Return all EnviDat metadata entries as Record objects.

Defaults to standard Record, content in json format.

**Args**

- **convert** (str) : Convert the content immediately to specified type.
  Options: "str", "xml", "iso", "bibtex", "dif", "datacite", "ris", "dcat-ap"
- **content_only** (bool) : Extract content from Record objects.

**Returns**

- Of Record entries for EnviDat metadata.

**Note**

and content_only is set to True.

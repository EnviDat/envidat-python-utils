#

## Record

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L31)

```python
Record(
   input_data: Union[str, dict], convert: Literal['str', 'xml', 'iso', 'bibtex',
   'dif', 'datacite', 'ris'] = None
)
```

---

Class manipulate an EnviDat record in various ways.

**Methods:**

### .get_content

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L92)

```python
.get_content()
```

---

Get current content of Record.

### .validate

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L96)

```python
.validate()
```

---

Validate metadata record.

### .to_json

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L156)

```python
.to_json()
```

---

Convert content to JSON string.

### .to_xml

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L160)

```python
.to_xml()
```

---

Convert content to XML record.

### .to_iso

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L164)

```python
.to_iso()
```

---

Convert content to ISO record.

### .to_ris

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L168)

```python
.to_ris()
```

---

Convert content to RIS format.

### .to_bibtex

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L172)

```python
.to_bibtex()
```

---

Convert content to BibTeX format.

### .to_dif

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L176)

```python
.to_dif()
```

---

Convert content to GCMD DIF 10.2 format.

### .to_datacite

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L180)

```python
.to_datacite(
   name_doi_map
)
```

---

Convert content to DataCite format.

---

### get_all_metadata_record_list

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/metadata.py/#L185)

```python
.get_all_metadata_record_list(
   convert: Literal['str', 'xml', 'iso', 'bibtex', 'dif', 'datacite',
   'ris'] = None, content_only: bool = False
)
```

---

Return all EnviDat metadata entries as Record objects.

Defaults to standard Record, content in json format.

**Args**

- Convert
  the content immediately to specified type.
- **content_only** (bool) : Extract content from Record objects.

**Returns**

- **list** : Of Record entries for EnviDat metadata.

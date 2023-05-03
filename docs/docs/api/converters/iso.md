#

### convert_iso

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/iso_converter.py/#L18)

```python
.convert_iso(
   metadata_record: dict
)
```

---

Generate XML formatted string compatible with ISO19139 standard.

**Note**

Converter is only valid for the metadata schema for EnviDat.

**Args**

- **metadata_record** (dict) : Individual EnviDat metadata entry record dictionary.

**Returns**

- **str** : XML formatted string compatible with ISO9139 standard.

---

### get_iso_language_code

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/iso_converter.py/#L522)

```python
.get_iso_language_code(
   code: str
)
```

---

Translate to language to 3-letter code.

http://www.loc.gov/standards/iso639-2/ISO-639-2_utf-8.txt

---

### get_or_missing

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/iso_converter.py/#L531)

```python
.get_or_missing(
   data_dict: dict, tag, ignore_case: bool = False
)
```

---

TODO.

---

### get_publication_date

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/iso_converter.py/#L559)

```python
.get_publication_date(
   data_dict: dict
)
```

---

Take date of type available or the publication year.

**Returns**

- **str** : Publication date from dataset, in string format.

---

### get_online_resource

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/iso_converter.py/#L617)

```python
.get_online_resource(
   url: str, name: str, function: str = 'download'
)
```

---

Create an online resource digital transfer element.

---

### is_url

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/iso_converter.py/#L643)

```python
.is_url(
   url_str
)
```

---

Check if string is URL.

Replicates functionality of CKAN method ckan.lib.helpers.is_url()

**Returns**

- **bool** : True if argument parses as a http, https or ftp URL,
  else returns False.

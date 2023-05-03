#

### convert_dif

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/dif_converter.py/#L16)

```python
.convert_dif(
   metadata_record: dict
)
```

---

Generate GCMD DIF 10.2 formatted XML string.

**Note**

Converter is only valid for the metadata schema for EnviDat.

**Args**

- **metadata_record** (dict) : Individual EnviDat metadata entry record dictionary.

**Returns**

- **str** : XML formatted string compatible with GCMD DIF 10.2 standard

---

### get_keywords

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/dif_converter.py/#L447)

```python
.get_keywords(
   data_dict
)
```

---

Extract keywords from tags.

---

### get_science_keywords

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/dif_converter.py/#L456)

```python
.get_science_keywords(
   data_dict, extras_dict
)
```

---

Guess keywords from organization.

---

### get_ignore_case

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/dif_converter.py/#L600)

```python
.get_ignore_case(
   data_dict, tag, ignore_blanks = True
)
```

---

Get value, case agnostic.

---

### extras_as_dict

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/dif_converter.py/#L616)

```python
.extras_as_dict(
   extras
)
```

---

Extract API 'extras' field as a simple dictionary.

---

### get_resource_formats

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/dif_converter.py/#L624)

```python
.get_resource_formats(
   dataset_dict
)
```

---

Get resource formats.

---

### get_resource_restrictions

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/dif_converter.py/#L638)

```python
.get_resource_restrictions(
   dataset_dict
)
```

---

Get resource restrictions.

---

### get_dif_language_code

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/dif_converter.py/#L654)

```python
.get_dif_language_code(
   code
)
```

---

Translate codes to language full word.

https://gcmd.nasa.gov/DocumentBuilder/defaultDif10/guide/data_set_language.html

Options: English; Afrikaans; Arabic; Bosnia; Bulgarian; Chinese; Croation; Czech;
Danish; Dutch; Estonian; Finnish; French; German; Hebrew; Hungarian; Indonesian;
Italian; Japanese; Korean; Latvian; Lithuanian; Norwegian; Polish; Portuguese;
Romanian; Russian; Slovak; Spanish; Ukrainian; Vietnamese

---

### get_bounding_rectangle

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/dif_converter.py/#L674)

```python
.get_bounding_rectangle(
   coordinates: list
)
```

---

Geometry bounding rectangle as coordinate list.

---

### get_bounding_rectangle_dict

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/dif_converter.py/#L691)

```python
.get_bounding_rectangle_dict(
   spatial_dict: dict
)
```

---

Geometry bounding rectangle as value dictionary.

---

### is_counter_clockwise

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/dif_converter.py/#L715)

```python
.is_counter_clockwise(
   points
)
```

---

Check if polygon is counterclockwise / valid.

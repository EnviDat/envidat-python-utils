#

### convert_xml

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/xml_converter.py/#L13)

```python
.convert_xml(
   package: dict
)
```

---

Convert EnviDat record to XML format.

**Args**

- **package** (dict) : Package JSON from API.

**Returns**

- **str** : XML formatted string.

---

### convert_xml_all_resources

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/xml_converter.py/#L35)

```python
.convert_xml_all_resources()
```

---

Convert EnviDat JSON records to XML format.

**Returns**

- **str** : XML formatted string.

**Note**

Only valid for metadata schema of EnviDat.

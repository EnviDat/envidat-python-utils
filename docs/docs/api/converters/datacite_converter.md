#

### convert_datacite

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/datacite_converter.py/#L17)

```python
.convert_datacite(
   package_json: str
)
```

---

Generate XML formatted string in DataCite format.

**Note**

Converter is only valid for the metadata schema for EnviDat.

**Args**

- **package_json** (str) : Individual EnviDat metadata entry record in JSON format.

**Returns**

- **str** : XML formatted string compatible with DataCite DIF 10.2 standard

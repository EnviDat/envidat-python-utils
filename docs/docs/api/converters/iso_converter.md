#

### convert_iso

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/iso_converter.py/#L18)

```python
.convert_iso(
   package_json: str
)
```

---

Generate XML formatted string compatible with ISO19139 standard.

**Note**

Converter is only valid for the metadata schema for EnviDat.

**Args**

- **package_json** (str) : Individual EnviDat metadata entry record in JSON format.

**Returns**

- **str** : XML formatted string compatible with ISO9139 standard.

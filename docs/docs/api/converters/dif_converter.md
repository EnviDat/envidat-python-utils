#

### convert_dif

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/dif_converter.py/#L16)

```python
.convert_dif(
   package_json: str
)
```

---

Generate GCMD DIF 10.2 formatted XML string.

**Note**

Converter is only valid for the metadata schema for EnviDat.

**Args**

- **package_json** (str) : Individual EnviDat metadata entry record in JSON format.

**Returns**

- **str** : XML formatted string compatible with GCMD DIF 10.2 standard

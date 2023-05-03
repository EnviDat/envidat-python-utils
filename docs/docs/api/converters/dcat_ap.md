#

### convert_dcat_ap

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/dcat_ap_converter.py/#L14)

```python
.convert_dcat_ap(
   metadata_records: Union[dict, list[dict]]
)
```

---

Generate output string in DCAT-AP format.

Accepts a single metadata entry, or list of entries.

**Note**

Converter is only valid for the metadata schema for EnviDat.

**Args**

metadata_records (dict, list[dict]):
Either: - Individual EnviDat metadata entry dictionary. - List of EnviDat metadata record dictionaries.

**Returns**

- **str** : string in DCAT-AP CH XML format.

---

### get_distribution_list

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/dcat_ap_converter.py/#L211)

```python
.get_distribution_list(
   metadata_record: dict, package_name: str
)
```

---

Return distribution_list created from package resources list and licence_id.

---

### wrap_packages_dcat_ap_xml

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/dcat_ap_converter.py/#L325)

```python
.wrap_packages_dcat_ap_xml(
   dcat_xml_packages: list
)
```

---

Add required DCAT-AP catalog XML tags for full DCAT-AP XML.

**Args**

- **dcat_xml_packages** (list[str,dict]) : All DCAT-AP formatted packages to include.
  In string XML or dictionary format.

**Note**

This is a required final step for producing a DCAT-AP CH format XML.

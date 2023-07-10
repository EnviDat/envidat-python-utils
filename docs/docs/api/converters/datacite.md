#

### convert_datacite

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/datacite_converter.py/#L25)

```python
.convert_datacite(
   metadata_record: dict
)
```

---

Generate XML formatted string in DataCite format.

**Note**

Converter is only valid for the metadata schema for EnviDat.

**Args**

- **metadata_record** (dict) : EnviDat metadata entry record dictionary.

**Returns**

- **str** : XML formatted string compatible with DataCite DIF 10.2 standard

---

### get_config_datacite_converter

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/datacite_converter.py/#L60)

```python
.get_config_datacite_converter()
```

---

Return validated datacite converter JSON config as Python dictionary.

Dictionary maps Datacite XML schema tags (keys) to EnviDat schema fields
(values).

**Returns**

- **dict** : datacite converter JSON config as Python dictionary
- **None** : if config failed validation

---

### get_dc_creator

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/datacite_converter.py/#L517)

```python
.get_dc_creator(
   author: dict, config: dict
)
```

---

Returns author information in DataCite "creator" tag format.

---

### get_dc_contributor

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/datacite_converter.py/#L567)

```python
.get_dc_contributor(
   maintainer: dict, config: dict
)
```

---

Returns maintainer in DataCite "contributor" tag format with a
contributorType of "ContactPerson".

REQUIRED DataCite attribute for each "contributor": "contributorType",
(value assigned is "Contact Person")

---

REQUIRED DataCite property for each "contibutor": "contributorName"

REQUIRED DataCite property for each "nameIdentifier" property:
"nameIdentifierScheme" (default value is "ORCID")

---

### affiliation_to_dc

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/datacite_converter.py/#L631)

```python
.affiliation_to_dc(
   affiliation, config
)
```

---

Returns affiliation in DataCite "affiliation" tag format.

Uses config to map commonly used affiliations in EnviDat packages
(i.e. "WSL", "SLF") with long names of instiutions
and ROR identifiers when available.

---

### get_dc_research_group

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/datacite_converter.py/#L687)

```python
.get_dc_research_group(
   organization_title
)
```

---

Returns organization title in DataCite "contributor" format with a
contributorType of "ResearchGroup".

---

### get_dc_related_identifiers

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/datacite_converter.py/#L703)

```python
.get_dc_related_identifiers(
   related_identifiers: str, has_related_datasets = False
)
```

---

Return EnviDat records "related_datasets" or "related_publications" values in
DataCite "relatedIdentifiers" tag format.

**Note**

"relatedIdentiferType" and "relationType" are required attributes
for each "relatedIdentifer"

**Args**

- **related_identifiers** (str) : Input related idetifiers, expected input is from
  "related_datasets" or "related_publications" keys.
- **has_related_datasets** (bool) : If true then input is assumed to be from
  "related_datasets" value in EnviDat record.
  Default value is false and is assumed to correspond to
  "related_publications" value in EnviDat record.

---

### get_dc_related_identifiers_resources

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/datacite_converter.py/#L792)

```python
.get_dc_related_identifiers_resources(
   resources
)
```

---

Return URLs from resources in DataCite "relatedIdentifier" tag format.

**Note**

"relatedIdentiferType" and "relationType" are required attributes
for each "relatedIdentifer"

---

### get_dc_formats

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/datacite_converter.py/#L815)

```python
.get_dc_formats(
   resources
)
```

---

Returns resources formats in DataCite "formats" tag format.

---

### get_dc_descriptions

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/datacite_converter.py/#L834)

```python
.get_dc_descriptions(
   notes, dc_description_type_tag, dc_xml_lang_tag
)
```

---

Returns notes in DataCite "descriptions" tag format.

"descriptionType" is a REQUIRED DataCite attribute for each "description",
(value assigned to "Abstract")

---

Logs warning for a description that is less than 100 characters.

---

### geometrycollection_to_dc_geolocations

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/datacite_converter.py/#L870)

```python
.geometrycollection_to_dc_geolocations(
   spatial: dict
)
```

---

Returns spatial data in DataCite "geoLocations" format.

Assumption: input spatial dictionary has a "type" value of "geometrycollection".

---

### get_dc_geolocations

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/datacite_converter.py/#L893)

```python
.get_dc_geolocations(
   spatial: dict, spatial_type: str = ''
)
```

---

Returns spatial data in DataCite "geoLocations" format.

For list of required attributes for each type of GeoLocation see DataCite documentation.

---

### get_doi

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/datacite_converter.py/#L1145)

```python
.get_doi(
   word: str
)
```

---

Get DOI string from input word string, if DOI not found then returns None.

**Example**

an input of "https://doi.org/10.1525/cse.2022.1561651" would return
"10.1525/cse.2022.1561651" as output

**Args**

- **word** (str) : Input string to test if it contains a DOI

**Returns**

- **str** : String of DOI
- **None** : If DOI could not be found

---

### get_envidat_doi

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/datacite_converter.py/#L1180)

```python
.get_envidat_doi(
   word: str, api_host = 'https: //envidat.ch',
   api_package_show = '/api/action/package_show?id = '
)
```

---

Get DOI string from input work by calling EnviDat API,
if DOI not found then returns None.

**Example**

An input of
"https://www.envidat.ch/#/metadata/amphibian-and-landscape-data-swiss-lowlands"
would return ""10.16904/envidat.267" as output

**Args**

- **word** (str) : Input string to test if it contains a DOI retrieved from
  EnviDat CKAN API
- **api_host** (str) : API host URL. Attempts to get from environment.
  Default value is "https://envidat.ch".
- **api_package_show** (str) : API host path to show package. Attempts to get from
  environment. Default value is "/api/action/package_show?id="

**Returns**

- **str** : String of DOI
- **None** : If DOI could not be found

---

### get_dora_doi

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/datacite_converter.py/#L1237)

```python
.get_dora_doi(
   word: str
)
```

---

Get DOI string from input word string by calling DORA API,
if DOI not found then returns None.

**Example**

an input of "https://www.dora.lib4ri.ch/wsl/islandora/object/wsl%3A3213"
would return "10.5194/tc-10-1075-2016" as output.

**Args**

- **word** (str) : Input string to test if it contains a DOI retrieved from DORA API

**Returns**

- **str** : String of DOI
- **None** : If DOI could not be found

---

### get_dora_doi_string

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/datacite_converter.py/#L1278)

```python
.get_dora_doi_string(
   dora_pid: str, dora_api_url: str = 'https: //envidat.ch/dora'
)
```

---

Get DOI string from WSL DORA API using DORA PID.

DORA API documentation:
https://www.wiki.lib4ri.ch/display/HEL/Technical+details+of+DORA

ASSUMPTION: Only one DOI exists in each DORA API record "citation" key

**Args**

- **dora_pid** (str) : DORA PID (permanent identification)
- **dora_api_url** (str) : API host url. Attempts to get from environment.
  Defaults to "https://envidat.ch/dora"

**Returns**

- **str** : String of DOI
- **None** : If DOI could not be found

---

### validate_dc_config

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/converters/datacite_converter.py/#L1347)

```python
.validate_dc_config(
   datacite_config: dict
)
```

---

Validate DataCite config has DataCite required keys using jsonschema.

**Note**

There are other DataCite required properties not included in this schema that
are handled differently in the converter (such as using default values).

---

Returns jsonschema.exceptions.ValidationError if input config invalid with schema.

**Args**

- **datacite_config** (dict) : dictionary derived from "datacite_converter"
  object in JSON config

**Returns**

- **None** : if datacite_config is valid against schema
- **ValidationError** : if datacite_config is invalid

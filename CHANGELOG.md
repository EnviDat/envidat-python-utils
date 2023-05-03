# CHANGELOG

## 1.4.0 (2023-05-03)

### Feat

- finish script datacite_updater_records.py
- add function to update just some records in DataCite in datacite_updater.py
- start working on new script to update some records in DataCite
- add geometrycollection spatial data processing in datacite_converter.py
- implement is_update arg to DataCite publish endpoint
- add optional cookie arg to CKAN API call
- added script and functions to import all records to DataCite
- add get_published_record_names_with_dois() to datacite_publisher.py
- add get_envidat_dois() to datacite_publisher.py
- add get_response_json() to email.utils.py
- validate args sent to email
- get user name and email from CKAN helper function
- add publish email template
- add enum classes and logic for publish actions and publish subjects
- add Jinga2 templates to send_email.py
- add endpoints that send email with FastMail
- implement SMPT emails
- start implementing notification emails
- implement FastApi and router to publish records in datacite
- implement jsonschema with datacite_converter config
- handle failed conversions in datacite converter
- add update logic to datacite publisher
- add validation for creators in datacite converter
- add datacite publisher functionality
- add reserve datacite doi functionality
- add helper funciton do DataCite published
- start code for publishing packages to DataCite API
- finish "affiliation" tags helper funciton in datacite converter
- add helper function to enhance "affiliation" tags in datacite converter
- add organization title to contributor tag in datacite converter
- add "schemeURI" attribute to creator and contributor tags in datacite converter
- add awardUrl tag to datacite converter
- add awardURI to datacite converter config
- add JSON config for converters
- add validators package
- extract DOI from DORA URL for Datacite converter

### Fix

- update log statements in datacite converter and importer
- correct search criteria in get_doi() in datacite_converter.py
- correct PID extraction from DORA URL
- retrieve DataCite DOIs from non-test API
- added URL validator to awardURI in datacite_converter.py
- load config with "utf-8" encoding in datacite converter
- allow duplicate formats in datacite converter
- remove "language" from metadata validator

### Refactor

- remove fastapi related code into separate repo
- remove redundant files
- update imports
- remove dev endpoints
- update auth in get_user_show()
- update email endpoint
- improve and restructure error handling in datacite_updater.py
- update code formatting in datacite updater scripts
- update code formatting in datacite_updater.py
- improve error handling in datacite_update_records()
- update formatting, TODOs, and imports in datacite_publisher.py
- update code formatting in datacite_converter.py
- fix type in geometry collection helper in datacite_converter.py
- update func thats updates variable number of records in datacite_updater.py
- update comments in datacite_updater_all_records.py
- rename script to update all records with DataCite
- improve get_dc_geolocations() handling (WIP) in datacite_converter.py
- add return type annotations to helper functions in datacite_converter.py
- finished updated get_dc_related_identifiers() and helper functions
- update get_dc_related_identifiers() and helper functions in datacite_converter.py
- improve processing of relatedIdentifiers in datacite_converter.py
- improve get_dora_doi() in datacite_converter.py
- update comments in datacite_importer.py
- improve error handling and logging in DataCite publish endpoint
- remove counter logic from datacite_updater.py
- modify datacite_updater.py to only modify and not create new DOIs
- include DOI in error response
- temporarily omit "geometrycollection" spatial data from DataCite converter
- improved logging in datacite_updater.py
- move get_response_json() to envidat.utils.py
- improve arguments handling in email sender
- improve logging in email utility
- improve validation in email sender
- implement error handling in email utility
- update imports in main.py
- extract getting email and subject to email/utils.py
- move send_email_publish_async() to router_publish.py
- update publish actions and move Enum classes to constants.py
- update send email functions
- improve send email function
- rename publish functio in router_publish.py
- add default error message to publish_to_datacite()
- add default values for error handling in router_publish.py
- improve error handling in router_publish.py
- rename publish router
- add logging to 'date_type' and 'notes' keys handling in datacite converter
- update error handling for required keys in datacite converter
- move config_converters.json to config directory
- update error handling for required keys in datacite converter
- assign default values for required keys in datacite converter
- extract error message logging for required keys to helper function in datacite converter
- remove 'doi' arg from datacite publisher
- format geolocation tag code
- add resource links to datacite converter
- improve DORA DOI helper function in datacite converter
- remove unused "name_doi_map" arg from get_all_metadata_record_list()
- remove legacy function in datacite converter
- remove "name_doi_map" from convert_datacite() call
- update geolocations & funding tags in DataCite converter
- extract helper functions in Datacite converter
- update "dates" and "language" tags in Datacite converter
- update "contributors" tag logic in Datacite converter
- update relatedIdentifier logic in Datacite converter
- update datacite converter to use json config
- restructure datacite converter
- streamline "related_datasets" logic for Datacite converter
- update "related_datasets" logic for Datacite converter
- add related_publications to Datacite converter relatedIdentifiers

## 1.3.0 (2022-10-25)

### Feat

- add method to remove FULL_ACCESS rights for user
- add method to bucket to grant user full access

### Refactor

- add set_public_read to init if is_public specified

### Fix

- add exception for CORS accessed denied (wrong user)

## 1.2.4 (2022-10-19)

### Fix

- multipart error if empty bucket, add items_per_page to Bucket.size

## 1.2.3 (2022-10-19)

### Fix

- catch empty bucket case when using size()

### Refactor

- move all class and staticmethods from Bucket into MetaBucket
- move list_buckets method into MetaBucket class for auto mkgendocs

## 1.2.2 (2022-10-19)

### Fix

- add staticmethod to Bucket to list all s3 buckets from endpoint

## 1.2.1 (2022-10-19)

### Fix

- add func to determine size of Bucket (efficient pagination)

## 1.2.0 (2022-10-18)

### Fix

- type checking for dcat-ap final wrap

### Feat

- add dcat-ap (opendataswiss) to metadata Record class
- added opendataswiss converter and tests
- working metadata Record class, linking to converters
- add envidat metadata Record class for conversion to various open formats

### Refactor

- black and isort, update refs to dcat-ap
- rename opendataswiss converter --> dcat-ap
- update variable names, add strip() calls to Bibtex and Datacite coverters
- add additional author to repo
- strip "Abstract" string in DIF converter
- strip "Abstract" string in DIF converter
- converters replace json input with dict, datacite get doi mapping once only
- simplify metadata name:doi mapping getter
- run pre-commit format and linting on all converter code
- remove temp test file for converters
- add extract arg to metadata Record, set input to positional

## 1.1.0 (2022-09-29)

### Feat

- add converters and metadata Record class

## 1.0.3 (2022-07-12)

### Fix

- logger year format to 4 digit, for clarity in logs

## 1.0.2 (2022-07-01)

### Fix

- add s3 delete_dir functionality
- s3 issues with dir funcs, strip preceeding slash, add download_all

## 1.0.1 (2022-07-01)

### Fix

- double slash in path for upload dir with root

## 1.0.0 (2022-07-01)

### Fix

- make boto3 logging optional via environment variable

## 0.6.0 (2022-07-01)

### Fix

- fix s3 list_all function returning without file extensions

### Feat

- add rename_file function, fix minor docstring lint errors

## 0.5.1 (2022-06-15)

### Fix

- check if key exists in dest bucket, prior to transfer

## 0.5.0 (2022-06-14)

### Feat

- add s3 transfer function for efficient data move between buckets

## 0.4.3 (2022-06-13)

### Fix

- add check_file_exists function to bucket class

## 0.4.2 (2022-06-07)

### Fix

- add cors config allow all origins if public

### Refactor

- update license with envidat

## 0.4.1 (2022-06-03)

### Fix

- minor feat, add clean multipart function, sort imports

### Refactor

- use isort to sort all imports

## 0.4.0 (2022-06-03)

### Feat

- add upload and download directory functions for s3 bucket

### Refactor

- update setting bucket name and api host, allow env var override if set as func var

## 0.3.3 (2022-05-23)

### Fix

- remove logging secret keys, bugfix endpoint var, remove default utf8 decode

## 0.3.2 (2022-05-23)

### Fix

- minor feat, add bucket cors set and get, plus restructure tests

## 0.3.1 (2022-05-19)

### Fix

- move get_url to utils, add favicon to s3 static website

## 0.3.0 (2022-05-19)

### Feat

- add s3 bucket functions to list directories

## 0.2.1 (2022-05-18)

### Fix

- cases where env vars are set after bucket class import

## 0.2.0 (2022-05-17)

### Feat

- add static website config funcs, fix existing funcs
- add s3 bucket class and api helper functions

## 0.1.0 (2022-05-16)

### Feat

- REDACTED

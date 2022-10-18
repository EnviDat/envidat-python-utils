# CHANGELOG

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

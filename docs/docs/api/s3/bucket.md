#

## Bucket

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L21)

```python
Bucket(
   bucket_name: str = None, is_new: bool = False, is_public: bool = False
)
```

---

Class to handle S3 bucket transactions.
Handles boto3 exceptions with custom exception classes.

**Methods:**

### .create

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L188)

```python
.create()
```

---

Create the S3 bucket on the endpoint.
Method may be called directly to manipulate the boto3 Bucket object.

**Returns**

- A boto3 S3 Bucket object.

### .get

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L213)

```python
.get(
   key: str, response_content_type: str = None, decode: bool = False
)
```

---

Get an object from the bucket into a memory object.
Defaults to utf-8 decode, unless specified.

**Args**

- **key** (str) : The key, i.e. path within the bucket to get.
- **response_content_type** (str) : Content type to enforce on the response.
  Defaults to None.
- **decode** (bool) : Decodes using utf-8 if set. Useful for text based files.
  Defaults to None.

**Returns**

- **tuple** : (data, S3 Metadata dict).

### .put

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L256)

```python
.put(
   key: str, data: Union[str, bytes], content_type: str = None, metadata: dict = {}
)
```

---

Put an in memory object into the bucket.

**Args**

- **key** (str) : The key, i.e. path within the bucket to store as.
- **data** (Union[str, bytes]) : The data to store, can be bytes or string.
- **content_type** (str) : The mime type to store the data as.
  E.g. important for binary data or html text.
  Defaults to None.
- **metadata** (dict) : Dictionary of metadata.
  E.g. timestamp or organisation details as string type.
  Defaults to None.

**Returns**

- **dict** : Response dictionary from S3.

### .delete

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L300)

```python
.delete(
   key: str
)
```

---

Delete specified object of a given key.

**Args**

- **key** (str) : The key, i.e. path within the bucket to delete.

**Returns**

- **dict** : Response dictionary from S3.

### .upload_file

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L320)

```python
.upload_file(
   key: str, local_filepath: Union[str, Path]
)
```

---

Upload a local file to the bucket.
Transparently manages multipart uploads.

**Args**

- **key** (str) : The key, i.e. path within the bucket to store as.
- **local_filepath** (Union[str, Path]) : Path string or Pathlib object to upload.

**Returns**

- **bool** : True if success, False is failure.

### .download_file

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L358)

```python
.download_file(
   key: str, local_filepath: Union[str, Path]
)
```

---

Download S3 object to a local file.
Transparently manages multipart downloads.

**Args**

- **key** (str) : The key, i.e. path within the bucket to download from.
- **local_filepath** (Union[str, Path]) : Path string or Pathlib object to upload.

**Returns**

- **bool** : True if success, False is failure.

### .configure_static_website

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L391)

```python
.configure_static_website(
   index_file: str = 'index.html', error_file: str = 'error.html',
   include_icon: bool = True
)
```

---

Add static website hosting config to an S3 bucket.

**Note**

WARNING this will set all data to public read policy.

**Args**

- **index_file** (str) : Name of index html file displaying page content.
  Defaults to 'index.html'.
- **error_file** (str) : Name of error html file displaying error content.
  Defaults to 'error.html'.
- **include_icon** (bool) : Include the envidat favicon.ico for the bucket.
  Defaults to True.

**Returns**

- **bool** : True if success, False is failure.

### .generate_index_html

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L461)

```python
.generate_index_html(
   title: str, file_list: Union[list, str], index_file: str = 'index.html'
)
```

---

Write index file to root of S3 bucket, with embedded S3 download links.

**Args**

- **title** (str) : HTML title tag for page.
- **file_list** (Union[list, str]) : List of file name to generate access urls for.
- **index_file** (str) : Name of index html file displaying page content.
  Defaults to 'index.html'.

**Returns**

- **dict** : Response dictionary from index file upload.

### .list_all

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L526)

```python
.list_all()
```

---

Get a list of all objects in the bucket.

**Returns**

- **list** : List of s3.ObjectSummary dicts, containing object metadata.

### .list_dir

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L553)

```python
.list_dir(
   path: str = '', recursive: bool = False, file_type: str = '', names_only: bool = False
)
```

---

Get a list of all objects in a specific directory (s3 path).
Returns up to a max of 1000 values.

**Args**

- **path** (str) : The directory in the bucket.
  Defaults to root ("").
- **recursive** (bool) : To list all objects and subdirectory objects recursively.
  Defaults to False.
- **file_type** (str) : File extension to filter by, e.g. 'txt'
  Defaults to blank string ("").
- **names_only** (bool) : Remove file extensions and path,
  giving only the file name.
  Defaults to False.

**Returns**

- **list** : List of s3.ObjectSummary dicts, containing object metadata.

### .get_cors_config

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L630)

```python
.get_cors_config()
```

---

Get the CORS config for a bucket.

**Returns**

- **dict** : Response dictionary containing CORS config.

### .set_cors_config

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L652)

```python
.set_cors_config(
   origins: list = None, allow_all: bool = False
)
```

---

Set the CORS config for a bucket.

**Args**

- **origins** (list) : List of allowed origins in CORS headers.
  Defaults to None.
- **allow_all** (bool) : Allow all origins, set to wildcard \*.
  Defaults to False

**Returns**

- **bool** : True if success, False is failure.

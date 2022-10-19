#

## Bucket

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L27)

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

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L195)

```python
.create()
```

---

Create the S3 bucket on the endpoint.

Method may be called directly to manipulate the boto3 Bucket object.

**Returns**

- A boto3 S3 Bucket object.

### .get

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L225)

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

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L268)

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

### .delete_file

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L311)

```python
.delete_file(
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

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L330)

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
- **local_filepath** (Union[str, Path]) : Path string or Pathlib path to upload.

**Returns**

- **bool** : True if success, False is failure.

### .download_file

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L368)

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
- **local_filepath** (Union[str, Path]) : Path string or Pathlib path
  to download to.

**Returns**

- **bool** : True if success, False is failure.

### .transfer

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L402)

```python
.transfer(
   source_key: str, dest_bucket: str, dest_key: str = None
)
```

---

Fast efficient transfer bucket --> bucket using TransferManager.

This function avoids downloading to memory and uses the underlying
operations that aws-cli uses to transfer.

**Args**

- **source_key** (str) : The key / path to copy from.
- **dest_bucket** (str) : Name of the destination bucket.
- **dest_key** (str) : The key / path to copy to.
  Optional, defaults to None.

**Returns**

- **bool** : True if success, False is failure.

### .list_all

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L452)

```python
.list_all()
```

---

Get a list of all objects in the bucket.

**Returns**

- **list** : All keys in the bucket.

### .list_dir

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L478)

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

### .download_dir

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L555)

```python
.download_dir(
   s3_path: str, local_dir: Union[str, Path], file_type: str = ''
)
```

---

Download an entire S3 path, including subpaths, to a local directory.

**Args**

- **s3_path** (str) : The path within the bucket to download.
- **local_dir** (Union[str, Path]) : Directory to download files into.
- **file_type** (str) : Download files with extension only, e.g. txt.

**Returns**

- **dict** : key:value pair of s3_key:download_status.
  download_status True if downloaded, False if failed.

### .download_all

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L591)

```python
.download_all(
   local_dir: Union[str, Path], file_type: str = ''
)
```

---

Download an entire S3 bucket, including subpaths, to a local directory.

**Args**

- **local_dir** (Union[str, Path]) : Directory to download files into.
- **file_type** (str) : Download files with extension only, e.g. txt.

**Returns**

- **dict** : key:value pair of s3_key:download_status.
  download_status True if downloaded, False if failed.

### .upload_dir

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L611)

```python
.upload_dir(
   local_dir: Union[str, Path], s3_path: str = '/', file_type: str = '',
   contents_only: bool = False
)
```

---

Upload the content of a local directory to a bucket path.

**Args**

- **local_dir** (Union[str, Path]) : Directory to upload files from.
- **s3_path** (str, optional) : The path within the bucket to upload to.
  If omitted, the bucket root is used.
- **file_type** (str, optional) : Upload files with extension only, e.g. txt.
- **contents_only** (bool) : Used to copy only the directory contents to the
  specified path, not the directory itself.

**Returns**

- **dict** : key:value pair of file_name:upload_status.
  upload_status True if uploaded, False if failed.

### .delete_dir

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L661)

```python
.delete_dir(
   s3_path: str, file_type: str = ''
)
```

---

Delete an entire S3 path, including subpaths.

USE WITH CAUTION!

**Args**

- **s3_path** (str) : The path within the bucket to delete.
- **file_type** (str) : Delete files with extension only, e.g. txt.

**Returns**

- **dict** : key:value pair of s3_key:deletion_status.
  deletion_status True if deleted, False if failed.

### .check_file_exists

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L696)

```python
.check_file_exists(
   key: str
)
```

---

Check an object exists in the bucket.

**Args**

- **key** (str) : The key, i.e. path within the bucket to check for.

**Returns**

- **bool** : True if exists, False if not.

### .rename_file

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L726)

```python
.rename_file(
   key: str, dest_key: str
)
```

---

Rename a file in a bucket, i.e. move then delete source.

**Args**

- **key** (str) : The key, i.e. path within the bucket.
- **dest_key** (str) : The key destination to move to.

**Returns**

- **bool** : True if success, False if skipped or failure.

### .clean_multiparts

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L761)

```python
.clean_multiparts()
```

---

Clean up failed multipart uploads in a bucket.

**Returns**

- **dict** : key:value pair of s3_multipart_key:clean_status.
  clean_status True if removed, False if failed.

### .size

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L809)

```python
.size()
```

---

Return the total size of a bucket, in bytes.

Uses a paginator to get around 1000 file limit for listing.

**Returns**

- **int** : Total size of all objects in bucket, in bytes.

### .configure_static_website

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L841)

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

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L910)

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

### .get_cors_config

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L974)

```python
.get_cors_config()
```

---

Get the CORS config for a bucket.

**Returns**

- **dict** : Response dictionary containing CORS config.

### .set_cors_config

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/bucket.py/#L995)

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
  Origins must be in format {schema}://{domain}:{port}.
- **allow_all** (bool) : Allow all origins, set to wildcard \*.
  Defaults to False

**Returns**

- **bool** : True if success, False is failure.

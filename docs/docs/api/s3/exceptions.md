#

## BucketException

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/exceptions.py/#L9)

```python
BucketException(
   message, bucket
)
```

---

Parent class to be inherited for consistency.

---

## NoSuchKey

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/exceptions.py/#L19)

```python
NoSuchKey(
   key, bucket
)
```

---

Exception for if bucket key does not exist.

---

## NoSuchBucket

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/exceptions.py/#L29)

```python
NoSuchBucket(
   bucket_name
)
```

---

Exception for if bucket does not exist.

---

## BucketAlreadyExists

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/exceptions.py/#L38)

```python
BucketAlreadyExists(
   bucket_name
)
```

---

Exception for if bucket already exists.

---

## BucketAccessDenied

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/exceptions.py/#L47)

```python
BucketAccessDenied(
   bucket_name
)
```

---

Exception for if bucket access is denied.

---

## NoSuchCORSConfiguration

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/exceptions.py/#L56)

```python
NoSuchCORSConfiguration(
   bucket_name
)
```

---

Exception for if the bucket does not have a CORS configuration.

---

## UnknownBucketException

[source](https://github.com/EnviDat/envidat-python-utils/blob/main/../envidat/s3/exceptions.py/#L65)

```python
UnknownBucketException(
   bucket_name, e: ClientError
)
```

---

Exception to catch all other unknown errors.

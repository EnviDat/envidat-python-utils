from moto import mock_s3
from tempfile import NamedTemporaryFile


# Clients
@mock_s3
def test_get_s3_resource(bucket):
    resource = bucket.get_boto3_resource()
    assert resource, "No boto3 resource was returned"


@mock_s3
def test_get_s3_client(bucket):
    client = bucket.get_boto3_client()
    assert client, "No boto3 client was returned"


# Bucket operations
@mock_s3
def test_bucket_create_public(bucket):
    bucket.is_public = True
    new_bucket = bucket.create()

    response = new_bucket.meta.client.head_bucket(Bucket="testing")
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200


@mock_s3
def test_bucket_put(bucket):
    bucket.create()

    file_text = "test"
    response = bucket.put("text.txt", file_text)
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200


@mock_s3
def test_bucket_get(bucket):
    bucket.create()

    file_text = "test"
    response = bucket.put("text.txt", file_text)
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    data, metadata = bucket.get("text.txt")
    assert data == "test"


@mock_s3
def test_bucket_delete(bucket):
    bucket.create()

    file_text = "test"
    response = bucket.put("text.txt", file_text)
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    response = bucket.delete("text.txt")
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 204


@mock_s3
def test_bucket_upload(bucket):
    bucket.create()

    file_text = "test"
    with NamedTemporaryFile(delete=True, suffix=".txt") as upload:
        with open(upload.name, "w", encoding="UTF-8") as f:
            f.write(file_text)

        success = bucket.upload_file(upload.name, upload.name)

    assert success is True


@mock_s3
def test_bucket_download(bucket):
    bucket.create()

    file_text = "test"
    with NamedTemporaryFile(delete=True, suffix=".txt") as upload:
        with open(upload.name, "w", encoding="UTF-8") as f:
            f.write(file_text)

        success = bucket.upload_file(upload.name, upload.name)

    assert success is True

    with NamedTemporaryFile(delete=True, suffix=".txt") as download:
        success = bucket.download_file(upload.name, download.name)
        assert success is True

        with open(download.name, encoding="UTF-8") as f:
            assert f.read() == "test"


@mock_s3
def test_configure_static_website(bucket):
    bucket.create()

    success = bucket.configure_static_website()
    assert success is True


@mock_s3
def test_generate_index_html(bucket):
    bucket.create()

    response = bucket.generate_index_html("testing", "testing")
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

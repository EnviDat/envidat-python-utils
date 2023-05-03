import json

import pytest
from moto import mock_s3

from envidat.s3.bucket import Bucket
from envidat.s3.exceptions import NoSuchCORSConfiguration


@mock_s3
def test_get_s3_resource(bucket):
    resource = Bucket.get_boto3_resource()
    assert resource, "No boto3 resource was returned"


@mock_s3
def test_get_s3_client(bucket):
    client = Bucket.get_boto3_client()
    assert client, "No boto3 client was returned"


@mock_s3
def test_bucket_create_public(bucket):
    bucket.is_public = True
    new_bucket = bucket.create()
    # Must reset class variable override for other tests
    bucket.is_public = False

    response = new_bucket.meta.client.head_bucket(Bucket="testing")
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200


@mock_s3
def test_set_public_read(bucket):
    bucket.create()

    success = bucket.set_public_read()
    assert success is True

    client = bucket.get_boto3_client()
    response = client.get_bucket_policy(
        Bucket=bucket.bucket_name,
    )
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    policy = json.loads(response["Policy"])
    assert policy["Statement"][0]["Sid"] == "PublicRead"


@mock_s3
def test_grant_full_access(bucket):
    bucket.create()

    acl = bucket.grant_user_full_access("ffffffff")
    assert acl["Grants"][1]["Grantee"]["ID"] == "ffffffff"


@mock_s3
def test_remove_full_access(bucket):
    bucket.create()

    acl = bucket.grant_user_full_access("ffffffff")
    assert acl["Grants"][1]["Grantee"]["ID"] == "ffffffff"

    acl = bucket.remove_user_full_access("user_that_does_not_exist")
    assert acl["Grants"][1]["Grantee"]["ID"] == "ffffffff"

    acl = bucket.remove_user_full_access("ffffffff")
    assert len(acl["Grants"]) == 1


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


@mock_s3
def test_get_bucket_cors_unset(bucket):
    bucket.create()

    with pytest.raises(NoSuchCORSConfiguration):
        bucket.get_cors_config()


@mock_s3
def test_set_bucket_cors(bucket):
    bucket.create()

    bucket.set_cors_config(origins=["testsite.com", "testsite2.ch"])
    response = bucket.get_cors_config()
    assert response["AllowedOrigins"] == ["testsite.com", "testsite2.ch"]


@mock_s3
def test_set_bucket_cors_allow_all(bucket):
    bucket.create()

    bucket.set_cors_config(allow_all=True)
    response = bucket.get_cors_config()
    assert response["AllowedOrigins"] == ["*"]


@mock_s3
def test_clean_multiparts(bucket, create_tempfile):
    bucket.create()

    client = Bucket.get_boto3_client()
    assert client

    key = "/test.txt"

    response = client.create_multipart_upload(
        Bucket=bucket.bucket_name,
        Key=key,
    )
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    with create_tempfile("txt") as upload:
        upload.write(b"0" * 1024 * 1024 * 5)  # 5MB

        response = client.upload_part(
            Bucket=bucket.bucket_name,
            Key=key,
            PartNumber=1,
            UploadId=response["UploadId"],
            Body=upload,
        )
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    response = client.list_multipart_uploads(
        Bucket=bucket.bucket_name,
    )
    assert len(response["Uploads"]) == 1

    status_dict = bucket.clean_multiparts()
    assert status_dict[key] is True

    response = client.list_multipart_uploads(
        Bucket=bucket.bucket_name,
    )
    assert "Uploads" not in response, "The multipart clean failed."


@mock_s3
def test_clean_multiparts_empty_bucket(bucket):
    bucket.create()

    status_dict = bucket.clean_multiparts()
    assert status_dict == {}


@mock_s3
def test_get_bucket_size(bucket, create_tempfile):
    bucket.create()

    with create_tempfile("txt") as temp1:
        with open(temp1.name, "w") as w:
            for _n in range(0, 57):
                w.write(str(1))
                w.write(",")

        status = bucket.upload_file(temp1.name, temp1.name)
        assert status is True

    bucket_size = bucket.size()
    assert bucket_size == 114


@mock_s3
def test_get_bucket_size_empty(bucket):
    bucket.create()

    bucket_size = bucket.size()
    assert bucket_size == 0


@mock_s3
def test_get_bucket_many_page(bucket, create_tempfile):
    bucket.create()

    with create_tempfile("txt") as temp1:
        with open(temp1.name, "w") as w:
            for _n in range(0, 20):
                w.write(str(1))
                w.write(",")

        status = bucket.upload_file(temp1.name, temp1.name)
        assert status is True

    bucket_size = bucket.size(items_per_page=5)
    assert bucket_size == 40


@mock_s3
def test_list_buckets(bucket, bucket2):
    bucket.create()
    bucket2.create()

    all_buckets = Bucket.list_buckets()
    assert all_buckets == ["testing", "testing2"]

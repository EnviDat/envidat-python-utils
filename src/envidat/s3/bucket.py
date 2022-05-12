import os
import logging
import boto3

from typing import Any, NoReturn
from pathlib import Path
from botocore import Config
from botocore.exceptions import ClientError

from . import exceptions


log = logging.getLogger(__name__)


class Bucket:
    """
    Class to handle S3 bucket transactions.
    Handles boto3 exceptions with custom exception classes.
    """

    _AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY")
    _AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_KEY")
    _AWS_ENDPOINT = os.getenv("AWS_ENDPOINT")
    _AWS_REGION = os.getenv("AWS_REGION", default="")

    def __init__(self, bucket_name: str, create: bool = None, is_public: bool = False):

        log.debug(
            "S3 Bucket object instantiated. "
            f"Access key: {Bucket._AWS_ACCESS_KEY_ID} | "
            f"Secret key: {Bucket._AWS_SECRET_ACCESS_KEY} | "
            f"Endpoint: {Bucket._AWS_ENDPOINT} | "
            f"Region: {Bucket._AWS_REGION} | "
        )
        # Ensure credentials are configured
        if not Bucket._AWS_ACCESS_KEY_ID or not Bucket._AWS_SECRET_ACCESS_KEY:
            log.error("Bucket instantiated without access key and secret key set.")
            raise TypeError(
                "AWS access key ID and AWS Secret access key must be configured."
                "Set them with environment variables AWS_ACCESS_KEY and AWS_ACCESS_KEY"
                "or with Bucket.config(access_key, secret_key, endpoint, region)"
            )
        if bucket_name is None:
            log.debug("Getting bucket name from environment variable.")
            self.bucket_name = os.getenv("AWS_BUCKET_NAME")
        else:
            self.bucket_name = bucket_name

        self.is_public = is_public

        if create is not None:
            create()

    @classmethod
    def config(
        cls, access_key: str, secret_key: str, endpoint=None, region=None
    ) -> NoReturn:
        cls._AWS_ACCESS_KEY_ID = access_key
        cls._AWS_SECRET_ACCESS_KEY = secret_key
        cls._AWS_ENDPOINT = endpoint
        cls._AWS_REGION = region

    @staticmethod
    def _get_boto3_session() -> NoReturn:
        """
        Configure boto3 session.
        """

        session = boto3.Session(
            aws_access_key_id=Bucket._AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Bucket._AWS_SECRET_ACCESS_KEY,
            endpoint_url=Bucket._AWS_ENDPOINT,
            region_name=Bucket._AWS_REGION,
            config=Config(signature_version="s3v4"),
        )

        return session

    @staticmethod
    def get_boto3_resource() -> NoReturn:
        """
        Configure boto3 resource object.
        """

        _session = Bucket._get_boto3_session()
        resource = _session.resource("s3")

        return resource

    @staticmethod
    def get_boto3_client() -> NoReturn:
        """
        Cofigure boto3 client object.
        """

        _session = Bucket._get_boto3_session()
        resource = _session.client("s3")

        return resource

    def _handle_boto3_client_error(self, e: ClientError, key=None) -> NoReturn:
        """
        Handle boto3 ClientError.
        The exception type returned from the server is nested here.
        Refer to exceptions.py

        Parameters
        ----------
        e: The ClientError to handle
        key: The S3 object key. Default None.
        """
        error_code: str = e.response.get("Error").get("Code")

        log.debug(e.response)

        if error_code == "AccessDenied":
            raise exceptions.BucketAccessDenied(self.bucket_name)
        elif error_code == "NoSuchBucket":
            raise exceptions.NoSuchBucket(self.bucket_name)
        elif error_code == "NoSuchKey":
            raise exceptions.NoSuchKey(key, self.bucket_name)
        elif error_code == "BucketAlreadyExists":
            raise exceptions.BucketAlreadyExists(self.bucket_name)
        else:
            raise exceptions.UnknownBucketException(self.bucket_name, e)

    def _raise_file_not_found(self, file_path: str) -> NoReturn:
        """
        Raise error if expected file not found on disk.

        :param e: The path to the expected file.
        """

        msg = f"Referenced file not found on disk: {file_path}"
        log.error(msg)
        raise FileNotFoundError(msg)

    @staticmethod
    def create(self) -> dict:
        """
        Create an S3 bucket.
        """

        resource = Bucket.get_boto3_resource()

        try:
            log.debug("Creating bucket...")
            response = resource.create_bucket(
                ACL="public-read" if self.is_public else "private",
                Bucket=self.bucket_name,
                CreateBucketConfiguration={
                    "LocationConstraint": f"{Bucket._AWS_REGION}"
                },
                ObjectLockEnabledForBucket=False,
            )
            log.debug(f"Created bucket: {self.bucket_name}")
            return response
        except ClientError as e:
            self._handle_boto3_client_error(e)

    def get(
        self,
        key: str,
        response_content_type: str = None,
        response_encoding: str = "utf-8",
    ) -> (Any, dict):
        """
        Get an object from the bucket into a memory object.
        Defaults to utf-8 decode, unless specified.

        :param key: The key, i.e. path within the bucket to get.
        :param response_content_type: Content type to enforce on the response.

        :return: tuple of decoded data and a dict containing S3 object metadata.
        """

        resource = Bucket.get_boto3_resource()
        s3_object = resource.Object(self.bucket_name, key)

        try:
            log.debug(f"Getting S3 object with key {key}")
            if response_content_type:
                response = s3_object.get(ResponseContentType=response_content_type)
            else:
                response = s3_object.get()

            log.debug(
                f"Reading and decoding returned data with encoding {response_encoding}"
            )
            data = response.get("Body").read().decode(response_encoding)
            metadata: dict = response.get("Metadata")

            return data, metadata

        except ClientError as e:
            self._handle_boto3_client_error(e, key=key)

    def put(
        self,
        key: str,
        data: str | bytes,
        content_type: str = None,
        metadata: dict = {},
    ) -> dict:
        """
        Put an in memory object into the bucket.

        :param key: The key, i.e. path within the bucket to store as.
        :param data: The data to store, can be bytes or string.
        :param content_type: The mime type to store the data as.
            E.g. important for binary data or html text.
        :param metadata: Dictionary of metadata.
            E.g. timestamp or organisation details as string type.

        :return: Response dictionary from S3.
        """

        resource = Bucket.get_boto3_resource()
        s3_object = resource.Object(self.bucket_name, key)

        try:
            if content_type:
                response = s3_object.put(
                    Body=data, ContentType=content_type, Key=key, Metadata=metadata
                )
            else:
                response = s3_object.put(Body=data, Key=key, Metadata=metadata)
            return response

        except ClientError as e:
            self._handle_boto3_client_error(e, key=key)

    def delete(self, key: str) -> dict:
        """
        Delete specified object of a given key.

        :param key: The key, i.e. path within the bucket to delete.

        :return: Response dictionary from S3.
        """

        resource = Bucket.get_boto3_resource()
        s3_object = resource.Object(self.bucket_name, key)

        try:
            response = s3_object.delete()
            return response

        except ClientError as e:
            self._handle_boto3_client_error(e, key=key)

    def upload_file(self, local_filepath: str | Path, key: str) -> dict:
        """
        Upload a local file to the bucket.
        Transparently manages multipart uploads.

        :param key: The key, i.e. path within the bucket to store under.
        :param local_filepath: Path string or Pathlib object to upload.

        :return: Response dictionary from S3.
        """

        resource = Bucket.get_boto3_resource()
        s3_object = resource.Object(self.bucket_name, key)

        file_path = Path(local_filepath).resolve()
        if not file_path.is_file():
            self._raise_file_not_found(file_path)
        else:
            file_path = str(file_path)

        try:
            response = s3_object.upload_file(file_path)
            return response

        except ClientError as e:
            self._handle_boto3_client_error(e, key=key)

    def download_file(self, key: str, local_filepath: str | Path) -> dict:
        """
        Download S3 object to a local file.
        Transparently manages multipart downloads.

        :param key: The key, i.e. path within the bucket to store under.
        :param local_filepath: Path string or Pathlib object to download to.

        :return: Response dictionary from S3.
        """

        resource = Bucket.get_boto3_resource()
        s3_object = resource.Object(self.bucket_name, key)

        file_path = Path(local_filepath).resolve()
        if not file_path.is_file():
            self._raise_file_not_found(file_path)
        else:
            file_path = str(file_path)

        try:
            response = s3_object.download_file(file_path)
            return response

        except ClientError as e:
            self._handle_boto3_client_error(e, key=key)

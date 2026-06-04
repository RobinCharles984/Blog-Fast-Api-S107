import logging
from typing import Any, Dict, Optional
from uuid import uuid4

try:
    import boto3  # type: ignore
    from botocore.config import Config  # type: ignore
    _has_boto3 = True
except Exception:
    boto3 = None
    Config = None
    _has_boto3 = False

from config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    BUCKET_NAME,
    REGION_NAME,
    AWS_ENDPOINT_URL,
    STORAGE_PUBLIC_BASE_URL,
)


def _create_s3_client():
    if not _has_boto3:
        logging.getLogger(__name__).warning("boto3 not installed; S3 operations will be no-ops")

        class _DummyS3Client:
            def upload_fileobj(self, fileobj, bucket, key, ExtraArgs=None):
                return None

            def delete_object(self, Bucket, Key):
                return None

        return _DummyS3Client()

    client_kwargs: Dict[str, Any] = {
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
        "region_name": REGION_NAME,
    }

    if AWS_ENDPOINT_URL:
        client_kwargs["endpoint_url"] = AWS_ENDPOINT_URL
        if Config is not None:
            client_kwargs["config"] = Config(s3={"addressing_style": "path"})

    return boto3.client("s3", **client_kwargs)


s3 = _create_s3_client()


def _build_url(filename: str) -> str:
    if STORAGE_PUBLIC_BASE_URL:
        return f"{STORAGE_PUBLIC_BASE_URL.rstrip('/')}/{filename}"
    return f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{filename}"


def upload_image_to_s3(file):
    filename = f"posts/{uuid4().hex}_{file.filename}"
    s3.upload_fileobj(file.file, BUCKET_NAME, filename, ExtraArgs={"ContentType": file.content_type})
    return _build_url(filename)


def delete_s3_file(file_url):
    if STORAGE_PUBLIC_BASE_URL:
        base = STORAGE_PUBLIC_BASE_URL.rstrip("/")
        file_key = file_url.replace(f"{base}/", "", 1)
    else:
        file_key = file_url.split(f"{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/")[-1]

    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=file_key)
    except Exception:
        pass

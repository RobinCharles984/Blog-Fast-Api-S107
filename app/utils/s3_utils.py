import boto3
from botocore.config import Config
from typing import Any, Dict
from uuid import uuid4

from config import (
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,
    BUCKET_NAME, REGION_NAME,
    AWS_ENDPOINT_URL, STORAGE_PUBLIC_BASE_URL,
)

_client_kwargs: Dict[str, Any] = {
    "aws_access_key_id": AWS_ACCESS_KEY_ID,
    "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
    "region_name": REGION_NAME,
}

if AWS_ENDPOINT_URL:
    _client_kwargs["endpoint_url"] = AWS_ENDPOINT_URL
    _client_kwargs["config"] = Config(s3={"addressing_style": "path"})

s3 = boto3.client("s3", **_client_kwargs)


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

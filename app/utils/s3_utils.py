import logging
try:
    import boto3  # type: ignore
    _has_boto3 = True
except Exception:
    boto3 = None
    _has_boto3 = False

from uuid import uuid4
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET_NAME, REGION_NAME

if _has_boto3:
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION_NAME
    )
else:
    logging.getLogger(__name__).warning("boto3 not installed; S3 operations will be no-ops")

    class _DummyS3Client:
        def upload_fileobj(self, fileobj, bucket, key, ExtraArgs=None):
            return None

        def delete_object(self, Bucket, Key):
            return None

    s3 = _DummyS3Client()


def upload_image_to_s3(file):
    filename = f"posts/{uuid4().hex}_{file.filename}"
    s3.upload_fileobj(file.file, BUCKET_NAME, filename, ExtraArgs={"ContentType": file.content_type})
    url = f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{filename}"
    return url


def delete_s3_file(file_url):
    file_key = file_url.split(f"{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/")[-1]

    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=file_key)
    except Exception:
        pass

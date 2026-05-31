from io import BytesIO
from unittest.mock import MagicMock, patch

import pytest

from app.utils.s3_utils import delete_s3_file, upload_image_to_s3
from config import BUCKET_NAME, REGION_NAME


def make_mock_upload_file(filename="photo.jpg", content_type="image/jpeg"):
    mock_file = MagicMock()
    mock_file.filename = filename
    mock_file.content_type = content_type
    mock_file.file = BytesIO(b"fake image content")
    return mock_file


class TestUploadImageToS3:
    @patch("app.utils.s3_utils.s3")
    def test_upload_calls_upload_fileobj(self, mock_s3):
        mock_file = make_mock_upload_file()
        upload_image_to_s3(mock_file)
        mock_s3.upload_fileobj.assert_called_once()

    @patch("app.utils.s3_utils.s3")
    def test_upload_passes_correct_content_type(self, mock_s3):
        mock_file = make_mock_upload_file(content_type="image/png")
        upload_image_to_s3(mock_file)
        _, kwargs = mock_s3.upload_fileobj.call_args
        assert kwargs["ExtraArgs"]["ContentType"] == "image/png"

    @patch("app.utils.s3_utils.s3")
    def test_upload_returns_url_with_bucket_and_region(self, mock_s3):
        mock_file = make_mock_upload_file()
        url = upload_image_to_s3(mock_file)
        assert BUCKET_NAME in url
        assert REGION_NAME in url

    @patch("app.utils.s3_utils.s3")
    def test_upload_returns_url_with_filename(self, mock_s3):
        mock_file = make_mock_upload_file(filename="myimage.jpg")
        url = upload_image_to_s3(mock_file)
        assert "myimage.jpg" in url

    @patch("app.utils.s3_utils.s3")
    def test_upload_url_starts_with_https(self, mock_s3):
        mock_file = make_mock_upload_file()
        url = upload_image_to_s3(mock_file)
        assert url.startswith("https://")

    @patch("app.utils.s3_utils.s3")
    def test_upload_stores_in_posts_folder(self, mock_s3):
        mock_file = make_mock_upload_file()
        upload_image_to_s3(mock_file)
        args, _ = mock_s3.upload_fileobj.call_args
        key = args[2]
        assert key.startswith("posts/")


class TestDeleteS3File:
    @patch("app.utils.s3_utils.s3")
    def test_delete_calls_delete_object(self, mock_s3):
        url = f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/posts/uuid_file.jpg"
        delete_s3_file(url)
        mock_s3.delete_object.assert_called_once()

    @patch("app.utils.s3_utils.s3")
    def test_delete_extracts_correct_key(self, mock_s3):
        key = "posts/abc123_photo.jpg"
        url = f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{key}"
        delete_s3_file(url)
        _, kwargs = mock_s3.delete_object.call_args
        assert kwargs["Key"] == key

    @patch("app.utils.s3_utils.s3")
    def test_delete_swallows_exception(self, mock_s3):
        mock_s3.delete_object.side_effect = Exception("S3 unavailable")
        url = f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/posts/file.jpg"
        # Should not raise
        delete_s3_file(url)

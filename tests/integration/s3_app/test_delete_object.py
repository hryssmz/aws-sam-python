# integration/s3_app/test_delete_object.py
from http import HTTPStatus
from urllib.parse import quote

import requests

from tests.integration.consts import API_PREFIX
from tests.unit.s3_app.consts import TEST_S3_BODY, TEST_S3_KEY
from tests.unit.s3_app.testutils import get_my_bucket, list_objects


def test_delete_object(clear_my_bucket: None) -> None:
    bucket = get_my_bucket()
    object = bucket.Object(TEST_S3_KEY)
    object.put(Body=TEST_S3_BODY.encode("utf-8"))

    assert list_objects() == [TEST_S3_KEY]

    encoded_key = quote(TEST_S3_KEY, safe="")
    url = f"{API_PREFIX}/objects/{encoded_key}"
    response = requests.delete(url)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert list_objects() == []

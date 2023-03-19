# s3_app/delete_object/test_integration.py
from http import HTTPStatus
import os
from urllib.parse import quote

import requests

from tests.s3_app.testutils import (
    TEST_S3_BODY,
    TEST_S3_KEY,
    get_my_bucket,
    list_objects,
)


def test_delete_object(clear_my_bucket: None) -> None:
    bucket = get_my_bucket()
    object = bucket.Object(TEST_S3_KEY)
    object.put(Body=TEST_S3_BODY.encode("utf-8"))

    assert list_objects() == [TEST_S3_KEY]

    encoded_key = quote(TEST_S3_KEY, safe="")
    url = f"{os.environ['REST_API_URL']}/objects/{encoded_key}"
    response = requests.delete(url)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert list_objects() == []

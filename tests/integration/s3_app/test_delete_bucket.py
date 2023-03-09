# integration/s3_app/test_delete_bucket.py
from http import HTTPStatus

import requests

from tests.integration.consts import API_PREFIX
from tests.unit.s3_app.consts import TEST_BUCKET
from tests.unit.s3_app.testutils import create_bucket, list_buckets


def test_delete_bucket(s3_fixture: None) -> None:
    create_bucket(TEST_BUCKET)

    assert TEST_BUCKET in list_buckets()

    url = f"{API_PREFIX}/buckets/{TEST_BUCKET}"
    response = requests.delete(url)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert TEST_BUCKET not in list_buckets()

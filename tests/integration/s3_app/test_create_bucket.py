# integration/s3_app/test_create_bucket.py
from http import HTTPStatus
import json

import jsonschema
import requests

from tests.integration.consts import API_PREFIX
from tests.unit.s3_app.consts import TEST_BUCKET
from tests.unit.s3_app.testutils import list_buckets
from tests.unit.schemas import EMPTY_OBJECT


def test_create_bucket(s3_fixture: None) -> None:
    url = f"{API_PREFIX}/buckets/{TEST_BUCKET}"
    response = requests.put(url)

    assert response.status_code == HTTPStatus.CREATED
    assert TEST_BUCKET in list_buckets()
    jsonschema.validate(json.loads(response.text), EMPTY_OBJECT)

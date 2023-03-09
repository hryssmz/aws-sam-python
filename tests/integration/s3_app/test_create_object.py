# integration/s3_app/test_create_object.py
from http import HTTPStatus
import json
from urllib.parse import quote

import jsonschema
import requests

from tests.integration.consts import API_PREFIX
from tests.unit.s3_app.consts import TEST_BUCKET, TEST_S3_BODY, TEST_S3_KEY
from tests.unit.s3_app.testutils import create_bucket, list_objects
from tests.unit.schemas import EMPTY_OBJECT


def test_create_object(s3_fixture: None) -> None:
    create_bucket(TEST_BUCKET)
    encoded_key = quote(TEST_S3_KEY, safe="")
    url = f"{API_PREFIX}/buckets/{TEST_BUCKET}/{encoded_key}"
    body = {"content": TEST_S3_BODY}
    response = requests.put(url, json=body)

    assert response.status_code == HTTPStatus.CREATED
    assert list_objects(TEST_BUCKET) == [TEST_S3_KEY]
    jsonschema.validate(json.loads(response.text), EMPTY_OBJECT)

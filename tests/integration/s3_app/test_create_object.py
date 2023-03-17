# integration/s3_app/test_create_object.py
from http import HTTPStatus
import json
from urllib.parse import quote

import jsonschema
import requests

from tests.integration.consts import API_PREFIX
from tests.unit.s3_app.consts import TEST_S3_BODY, TEST_S3_KEY
from tests.unit.s3_app.schemas import EMPTY_OBJECT
from tests.unit.s3_app.testutils import list_objects


def test_create_object(clear_my_bucket: None) -> None:
    encoded_key = quote(TEST_S3_KEY, safe="")
    url = f"{API_PREFIX}/objects/{encoded_key}"
    body = {"content": TEST_S3_BODY}
    response = requests.put(url, json=body)
    res_body = json.loads(response.text)

    assert response.status_code == HTTPStatus.CREATED
    assert list_objects() == [TEST_S3_KEY]

    jsonschema.validate(res_body, EMPTY_OBJECT)

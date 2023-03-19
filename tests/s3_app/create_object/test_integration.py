# s3_app/create_object/test_integration.py
from http import HTTPStatus
import json
import os
from urllib.parse import quote

import jsonschema
import requests

from tests.s3_app.schemas import EMPTY_OBJECT
from tests.s3_app.testutils import TEST_S3_BODY, TEST_S3_KEY, list_objects


def test_create_object(clear_my_bucket: None) -> None:
    encoded_key = quote(TEST_S3_KEY, safe="")
    url = f"{os.environ['REST_API_URL']}/objects/{encoded_key}"
    body = {"content": TEST_S3_BODY}
    response = requests.put(url, json=body)
    res_body = json.loads(response.text)

    assert response.status_code == HTTPStatus.CREATED
    assert list_objects() == [TEST_S3_KEY]

    jsonschema.validate(res_body, EMPTY_OBJECT)

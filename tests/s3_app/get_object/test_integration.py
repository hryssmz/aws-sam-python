# s3_app/get_object/test_integration.py
from http import HTTPStatus
import json
import os
from urllib.parse import quote

import jsonschema
import requests

from tests.s3_app.schemas import GET_OBJECT_RESPONSE
from tests.s3_app.testutils import TEST_S3_BODY, TEST_S3_KEY, get_my_bucket


def test_get_object(clear_my_bucket: None) -> None:
    bucket = get_my_bucket()
    object = bucket.Object(TEST_S3_KEY)
    object.put(Body=TEST_S3_BODY.encode("utf-8"))

    encoded_key = quote(TEST_S3_KEY, safe="")
    url = f"{os.environ['REST_API_URL']}/objects/{encoded_key}"
    response = requests.get(url)
    res_body = json.loads(response.text)

    assert response.status_code == HTTPStatus.OK
    assert res_body["content"] == TEST_S3_BODY

    jsonschema.validate(res_body, GET_OBJECT_RESPONSE)

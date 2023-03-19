# s3_app/list_objects/test_integration.py
from http import HTTPStatus
import json
import os

import jsonschema
import requests

from tests.s3_app.schemas import LIST_OBJECTS_RESPONSE
from tests.s3_app.testutils import TEST_S3_BODY, TEST_S3_KEY, get_my_bucket


def test_list_objects(clear_my_bucket: None) -> None:
    bucket = get_my_bucket()
    object = bucket.Object(TEST_S3_KEY)
    object.put(Body=TEST_S3_BODY.encode("utf-8"))

    url = f"{os.environ['REST_API_URL']}/objects"
    response = requests.get(url)
    res_body = json.loads(response.text)

    assert response.status_code == HTTPStatus.OK
    assert res_body["objects"] == [TEST_S3_KEY]

    jsonschema.validate(res_body, LIST_OBJECTS_RESPONSE)

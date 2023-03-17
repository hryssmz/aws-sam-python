# integration/s3_app/test_list_objects.py
from http import HTTPStatus
import json

import jsonschema
import requests

from tests.integration.consts import API_PREFIX
from tests.unit.s3_app.consts import TEST_S3_BODY, TEST_S3_KEY
from tests.unit.s3_app.schemas import LIST_OBJECTS_RESPONSE
from tests.unit.s3_app.testutils import get_my_bucket


def test_list_objects(clear_my_bucket: None) -> None:
    bucket = get_my_bucket()
    object = bucket.Object(TEST_S3_KEY)
    object.put(Body=TEST_S3_BODY.encode("utf-8"))

    url = f"{API_PREFIX}/objects"
    response = requests.get(url)
    res_body = json.loads(response.text)

    assert response.status_code == HTTPStatus.OK
    assert res_body["objects"] == [TEST_S3_KEY]

    jsonschema.validate(res_body, LIST_OBJECTS_RESPONSE)

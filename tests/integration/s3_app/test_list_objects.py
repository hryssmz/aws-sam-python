# integration/s3_app/test_list_objects.py
from http import HTTPStatus
import json

import jsonschema
import requests

from tests.integration.consts import API_PREFIX
from tests.unit.s3_app.consts import TEST_BUCKET, TEST_S3_BODY, TEST_S3_KEY
from tests.unit.s3_app.testutils import create_bucket
from tests.unit.schemas import GET_BUCKET_RESPONSE


def test_list_objects(s3_fixture: None) -> None:
    bucket = create_bucket(TEST_BUCKET)
    object = bucket.Object(TEST_S3_KEY)
    object.put(Body=TEST_S3_BODY.encode("utf-8"))

    url = f"{API_PREFIX}/buckets/{TEST_BUCKET}"
    response = requests.get(url)
    res_body = json.loads(response.text)

    assert response.status_code == HTTPStatus.OK
    assert res_body["objects"] == [TEST_S3_KEY]
    jsonschema.validate(res_body, GET_BUCKET_RESPONSE)

# unit/s3_app/list_objects/test_app.py
from http import HTTPStatus
import json

import jsonschema

from functions.s3_app.list_objects import app
from tests.unit.s3_app.consts import TEST_S3_BODY, TEST_S3_KEY
from tests.unit.s3_app.schemas import LIST_OBJECTS_RESPONSE
from tests.unit.s3_app.testutils import get_my_bucket
from tests.unit.testutils import get_dummy_apigw_event, get_dummy_context


def test_ok(clear_my_bucket: None) -> None:
    bucket = get_my_bucket()
    object = bucket.Object(TEST_S3_KEY)
    object.put(Body=TEST_S3_BODY.encode("utf-8"))

    event = get_dummy_apigw_event()
    context = get_dummy_context()
    response = app.handler(dict(event), context)
    res_body = json.loads(response["body"])

    assert response["statusCode"] == HTTPStatus.OK
    assert res_body["objects"] == [TEST_S3_KEY]
    jsonschema.validate(res_body, LIST_OBJECTS_RESPONSE)

# unit/s3_app/list_objects/test_app.py
from http import HTTPStatus
import json

import jsonschema

from functions.s3_app.list_objects import app
from tests.unit.s3_app.consts import (
    TEST_BUCKET,
    TEST_S3_BODY,
    TEST_S3_KEY,
    UNOWNED_BUCKET,
)
from tests.unit.s3_app.testutils import create_bucket
from tests.unit.schemas import CLIENT_ERROR, GET_BUCKET_RESPONSE
from tests.unit.testutils import get_dummy_apigw_event, get_dummy_context


def test_app(s3_fixture: None) -> None:
    event = get_dummy_apigw_event()
    event["pathParameters"] = {"bucket": TEST_BUCKET}
    context = get_dummy_context()
    response = app.handler(dict(event), context)

    assert response["statusCode"] == HTTPStatus.NOT_FOUND
    jsonschema.validate(json.loads(response["body"]), CLIENT_ERROR)

    bucket = create_bucket(TEST_BUCKET)
    object = bucket.Object(TEST_S3_KEY)
    object.put(Body=TEST_S3_BODY.encode("utf-8"))
    response = app.handler(dict(event), context)
    res_body = json.loads(response["body"])

    assert response["statusCode"] == HTTPStatus.OK
    assert res_body["objects"] == [TEST_S3_KEY]
    jsonschema.validate(res_body, GET_BUCKET_RESPONSE)


def test_forbidden() -> None:
    event = get_dummy_apigw_event()
    event["pathParameters"] = {"bucket": UNOWNED_BUCKET}
    context = get_dummy_context()
    response = app.handler(dict(event), context)

    assert response["statusCode"] == HTTPStatus.FORBIDDEN
    jsonschema.validate(json.loads(response["body"]), CLIENT_ERROR)

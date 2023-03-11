# unit/s3_app/create_object/test_app.py
from http import HTTPStatus
import json

import jsonschema

from functions.s3_app.create_object import app
from tests.unit.s3_app.consts import TEST_S3_BODY, TEST_S3_KEY
from tests.unit.s3_app.schemas import CLIENT_ERROR, EMPTY_OBJECT
from tests.unit.s3_app.testutils import list_objects
from tests.unit.testutils import get_dummy_apigw_event, get_dummy_context


def test_created(clear_my_bucket: None) -> None:
    event = get_dummy_apigw_event()
    event["pathParameters"] = {"key": TEST_S3_KEY}
    event["body"] = json.dumps({"content": TEST_S3_BODY})
    context = get_dummy_context()
    response = app.handler(dict(event), context)

    assert response["statusCode"] == HTTPStatus.CREATED
    assert list_objects() == [TEST_S3_KEY]
    jsonschema.validate(json.loads(response["body"]), EMPTY_OBJECT)


def test_bad_request() -> None:
    event = get_dummy_apigw_event()
    event["pathParameters"] = {"key": TEST_S3_KEY}
    event["body"] = json.dumps({})
    context = get_dummy_context()
    response = app.handler(dict(event), context)

    assert response["statusCode"] == HTTPStatus.BAD_REQUEST
    jsonschema.validate(json.loads(response["body"]), CLIENT_ERROR)

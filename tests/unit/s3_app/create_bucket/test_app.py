# unit/s3_app/create_bucket/test_app.py
from http import HTTPStatus
import json

import jsonschema

from functions.s3_app.create_bucket import app
from tests.unit.s3_app.consts import TEST_BUCKET, UNOWNED_BUCKET
from tests.unit.s3_app.testutils import list_buckets
from tests.unit.schemas import CLIENT_ERROR, EMPTY_OBJECT
from tests.unit.testutils import get_dummy_apigw_event, get_dummy_context


def test_app(s3_fixture: None) -> None:
    event = get_dummy_apigw_event()
    event["pathParameters"] = {"bucket": TEST_BUCKET}
    context = get_dummy_context()
    response = app.handler(dict(event), context)

    assert response["statusCode"] == HTTPStatus.CREATED
    assert TEST_BUCKET in list_buckets()
    jsonschema.validate(json.loads(response["body"]), EMPTY_OBJECT)

    response = app.handler(dict(event), context)

    assert response["statusCode"] == HTTPStatus.NO_CONTENT


def test_forbidden() -> None:
    event = get_dummy_apigw_event()
    event["pathParameters"] = {"bucket": UNOWNED_BUCKET}
    context = get_dummy_context()
    response = app.handler(dict(event), context)

    assert response["statusCode"] == HTTPStatus.FORBIDDEN
    jsonschema.validate(json.loads(response["body"]), CLIENT_ERROR)

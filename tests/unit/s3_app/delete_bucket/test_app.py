# unit/s3_app/delete_bucket/test_app.py
from http import HTTPStatus
import json

import jsonschema

from functions.s3_app.delete_bucket import app
from tests.unit.s3_app.consts import TEST_BUCKET, UNOWNED_BUCKET
from tests.unit.s3_app.testutils import create_bucket, list_buckets
from tests.unit.schemas import CLIENT_ERROR
from tests.unit.testutils import get_dummy_apigw_event, get_dummy_context


def test_app(s3_fixture: None) -> None:
    event = get_dummy_apigw_event()
    event["pathParameters"] = {"bucket": TEST_BUCKET}
    context = get_dummy_context()
    response = app.handler(dict(event), context)

    assert response["statusCode"] == HTTPStatus.NOT_FOUND
    jsonschema.validate(json.loads(response["body"]), CLIENT_ERROR)

    create_bucket(TEST_BUCKET)

    assert TEST_BUCKET in list_buckets()

    response = app.handler(dict(event), context)

    assert response["statusCode"] == HTTPStatus.NO_CONTENT
    assert TEST_BUCKET not in list_buckets()


def test_forbidden() -> None:
    event = get_dummy_apigw_event()
    event["pathParameters"] = {"bucket": UNOWNED_BUCKET}
    context = get_dummy_context()
    response = app.handler(dict(event), context)

    assert response["statusCode"] == HTTPStatus.FORBIDDEN
    jsonschema.validate(json.loads(response["body"]), CLIENT_ERROR)

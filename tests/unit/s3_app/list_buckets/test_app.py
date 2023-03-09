# unit/s3_app/list_buckets/test_app.py
from http import HTTPStatus
import json

import jsonschema

from functions.s3_app.list_buckets import app
from tests.unit.schemas import GET_BUCKETS_RESPONSE
from tests.unit.testutils import get_dummy_apigw_event, get_dummy_context


def test_app() -> None:
    event = get_dummy_apigw_event()
    context = get_dummy_context()
    response = app.handler(dict(event), context)

    assert response["statusCode"] == HTTPStatus.OK
    jsonschema.validate(json.loads(response["body"]), GET_BUCKETS_RESPONSE)

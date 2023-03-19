# hello_world_app/hello_world/test_unit.py
from http import HTTPStatus
import json

import jsonschema

from functions.hello_world_app.hello_world import app
from tests.hello_world_app.schemas import HELLO_WORLD_RESPONSE
from tests.hello_world_app.testutils import (
    get_dummy_apigw_event,
    get_dummy_context,
)


def test_ok() -> None:
    event = get_dummy_apigw_event()
    context = get_dummy_context()
    response = app.handler(dict(event), context)
    res_body = json.loads(response["body"])

    assert response["statusCode"] == HTTPStatus.OK
    assert res_body["message"] == "Hello World!"

    jsonschema.validate(res_body, HELLO_WORLD_RESPONSE)


def test_bad() -> None:
    assert 0 == 1

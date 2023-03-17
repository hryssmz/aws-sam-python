# unit/todo_app/get_todo/test_app.py
from http import HTTPStatus
import json
import uuid

import jsonschema

from functions.todo_app.get_todo import app
from tests.unit.testutils import get_dummy_apigw_event, get_dummy_context
from tests.unit.todo_app.consts import (
    TODO_DESCRIPTION,
    TODO_NAME,
    TODO_PRIORITY,
)
from tests.unit.todo_app.schemas import CLIENT_ERROR, GET_TODO_RESPONSE
from tests.unit.todo_app.testutils import create_todo


def test_ok(clear_todos: None) -> None:
    payload = {
        "name": TODO_NAME,
        "description": TODO_DESCRIPTION,
        "priority": TODO_PRIORITY,
    }
    id = create_todo(payload)

    event = get_dummy_apigw_event()
    event["pathParameters"] = {"id": id}
    context = get_dummy_context()
    response = app.handler(dict(event), context)
    res_body = json.loads(response["body"])

    assert response["statusCode"] == HTTPStatus.OK
    assert res_body["todo"]["id"] == id
    assert res_body["todo"]["name"] == TODO_NAME
    assert res_body["todo"]["description"] == TODO_DESCRIPTION
    assert res_body["todo"]["priority"] == TODO_PRIORITY
    jsonschema.validate(res_body, GET_TODO_RESPONSE)


def test_not_found(clear_todos: None) -> None:
    event = get_dummy_apigw_event()
    event["pathParameters"] = {"id": str(uuid.uuid4())}
    context = get_dummy_context()
    response = app.handler(dict(event), context)
    res_body = json.loads(response["body"])

    assert response["statusCode"] == HTTPStatus.NOT_FOUND

    jsonschema.validate(res_body, CLIENT_ERROR)

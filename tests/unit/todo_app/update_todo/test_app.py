# unit/todo_app/update_todo/test_app.py
from http import HTTPStatus
import json
import uuid

import jsonschema

from functions.todo_app.update_todo import app
from tests.unit.testutils import get_dummy_apigw_event, get_dummy_context
from tests.unit.todo_app.consts import (
    TODO_DESCRIPTION,
    TODO_NAME,
    TODO_PRIORITY,
)
from tests.unit.todo_app.schemas import CLIENT_ERROR, UPDATE_TODO_RESPONSE
from tests.unit.todo_app.testutils import create_todo


def test_ok(clear_todos: None) -> None:
    id = create_todo({"name": "dummy", "description": "", "priority": 2})
    event = get_dummy_apigw_event()
    event["pathParameters"] = {"id": id}
    event["body"] = json.dumps(
        {
            "name": TODO_NAME,
            "description": TODO_DESCRIPTION,
            "priority": TODO_PRIORITY,
        }
    )
    context = get_dummy_context()
    response = app.handler(dict(event), context)
    res_body = json.loads(response["body"])

    assert response["statusCode"] == HTTPStatus.OK
    assert res_body["todo"]["id"] == id
    assert res_body["todo"]["name"] == TODO_NAME
    assert res_body["todo"]["description"] == TODO_DESCRIPTION
    assert res_body["todo"]["priority"] == TODO_PRIORITY
    jsonschema.validate(res_body, UPDATE_TODO_RESPONSE)


def test_bad_request(clear_todos: None) -> None:
    event = get_dummy_apigw_event()
    event["pathParameters"] = {"id": str(uuid.uuid4())}
    event["body"] = json.dumps(
        {
            "name": TODO_NAME,
            "description": TODO_DESCRIPTION,
            "priority": 5,
        }
    )
    context = get_dummy_context()
    response = app.handler(dict(event), context)

    assert response["statusCode"] == HTTPStatus.BAD_REQUEST

    jsonschema.validate(json.loads(response["body"]), CLIENT_ERROR)


def test_not_found(clear_todos: None) -> None:
    event = get_dummy_apigw_event()
    event["pathParameters"] = {"id": str(uuid.uuid4())}
    event["body"] = json.dumps(
        {
            "name": TODO_NAME,
            "description": TODO_DESCRIPTION,
            "priority": TODO_PRIORITY,
        }
    )
    context = get_dummy_context()
    response = app.handler(dict(event), context)

    assert response["statusCode"] == HTTPStatus.NOT_FOUND

    jsonschema.validate(json.loads(response["body"]), CLIENT_ERROR)

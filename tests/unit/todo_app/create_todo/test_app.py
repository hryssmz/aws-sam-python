# unit/todo_app/create_todo/test_app.py
from http import HTTPStatus
import json

import jsonschema

from functions.todo_app.create_todo import app
from tests.unit.testutils import get_dummy_apigw_event, get_dummy_context
from tests.unit.todo_app.consts import (
    TODO_DESCRIPTION,
    TODO_NAME,
    TODO_PRIORITY,
)
from tests.unit.todo_app.schemas import CLIENT_ERROR, CREATE_TODO_RESPONSE
from tests.unit.todo_app.testutils import list_todos


def test_created_1(clear_todos: None) -> None:
    assert len(list_todos()) == 0

    event = get_dummy_apigw_event()
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

    assert response["statusCode"] == HTTPStatus.CREATED
    assert len(list_todos()) == 1
    assert res_body["todo"]["name"] == TODO_NAME
    assert res_body["todo"]["description"] == TODO_DESCRIPTION
    assert res_body["todo"]["priority"] == TODO_PRIORITY

    jsonschema.validate(res_body, CREATE_TODO_RESPONSE)


def test_created_2(clear_todos: None) -> None:
    assert len(list_todos()) == 0

    event = get_dummy_apigw_event()
    event["body"] = json.dumps({"name": TODO_NAME})
    context = get_dummy_context()
    response = app.handler(dict(event), context)
    res_body = json.loads(response["body"])

    assert response["statusCode"] == HTTPStatus.CREATED
    assert len(list_todos()) == 1
    assert res_body["todo"]["name"] == TODO_NAME
    assert res_body["todo"]["description"] == ""
    assert res_body["todo"]["priority"] == 2

    jsonschema.validate(res_body, CREATE_TODO_RESPONSE)


def test_bad_request_1() -> None:
    event = get_dummy_apigw_event()
    event["body"] = json.dumps({"description": TODO_DESCRIPTION})
    context = get_dummy_context()
    response = app.handler(dict(event), context)
    res_body = json.loads(response["body"])

    assert response["statusCode"] == HTTPStatus.BAD_REQUEST

    jsonschema.validate(res_body, CLIENT_ERROR)


def test_bad_request_2() -> None:
    event = get_dummy_apigw_event()
    event["body"] = json.dumps(
        {"name": TODO_NAME, "description": TODO_DESCRIPTION, "priority": 5}
    )
    context = get_dummy_context()
    response = app.handler(dict(event), context)
    res_body = json.loads(response["body"])

    assert response["statusCode"] == HTTPStatus.BAD_REQUEST

    jsonschema.validate(res_body, CLIENT_ERROR)

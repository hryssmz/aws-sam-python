# unit/todo_app/list_todos/test_app.py
from http import HTTPStatus
import json

import jsonschema

from functions.todo_app.list_todos import app
from tests.unit.testutils import get_dummy_apigw_event, get_dummy_context
from tests.unit.todo_app.consts import (
    TODO_DESCRIPTION,
    TODO_NAME,
    TODO_PRIORITY,
)
from tests.unit.todo_app.schemas import LIST_TODOS_RESPONSE
from tests.unit.todo_app.testutils import create_todo, list_todos


def test_ok(clear_todos: None) -> None:
    payload = {
        "name": TODO_NAME,
        "description": TODO_DESCRIPTION,
        "priority": TODO_PRIORITY,
    }
    create_todo(payload)

    assert len(list_todos()) == 1

    event = get_dummy_apigw_event()
    context = get_dummy_context()
    response = app.handler(dict(event), context)
    res_body = json.loads(response["body"])

    assert response["statusCode"] == HTTPStatus.OK
    assert len(res_body["todos"]) == 1
    assert res_body["todos"][0]["name"] == TODO_NAME
    assert res_body["todos"][0]["description"] == TODO_DESCRIPTION
    assert res_body["todos"][0]["priority"] == TODO_PRIORITY

    jsonschema.validate(res_body, LIST_TODOS_RESPONSE)

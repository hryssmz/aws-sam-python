# integration/todo_app/test_create_todo.py
from http import HTTPStatus
import json

import jsonschema
import requests

from tests.integration.consts import API_PREFIX
from tests.unit.todo_app.consts import (
    TODO_DESCRIPTION,
    TODO_NAME,
    TODO_PRIORITY,
)
from tests.unit.todo_app.schemas import CREATE_TODO_RESPONSE
from tests.unit.todo_app.testutils import list_todos


def test_create_todo(clear_todos: None) -> None:
    assert len(list_todos()) == 0

    url = f"{API_PREFIX}/todos"
    body = {
        "name": TODO_NAME,
        "description": TODO_DESCRIPTION,
        "priority": TODO_PRIORITY,
    }
    response = requests.post(url, json=body)
    res_body = json.loads(response.text)

    assert response.status_code == HTTPStatus.CREATED
    assert len(list_todos()) == 1
    assert res_body["todo"]["name"] == TODO_NAME
    assert res_body["todo"]["description"] == TODO_DESCRIPTION
    assert res_body["todo"]["priority"] == TODO_PRIORITY

    jsonschema.validate(res_body, CREATE_TODO_RESPONSE)

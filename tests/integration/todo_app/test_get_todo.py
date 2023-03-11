# integration/todo_app/test_get_todo.py
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
from tests.unit.todo_app.schemas import GET_TODO_RESPONSE
from tests.unit.todo_app.testutils import create_todo


def test_get_todo(clear_todos: None) -> None:
    payload = {
        "name": TODO_NAME,
        "description": TODO_DESCRIPTION,
        "priority": TODO_PRIORITY,
    }
    id = create_todo(payload)

    url = f"{API_PREFIX}/todos/{id}"
    response = requests.get(url)
    res_body = json.loads(response.text)

    assert response.status_code == HTTPStatus.OK
    assert res_body["todo"]["id"] == id
    assert res_body["todo"]["name"] == TODO_NAME
    assert res_body["todo"]["description"] == TODO_DESCRIPTION
    assert res_body["todo"]["priority"] == TODO_PRIORITY
    jsonschema.validate(res_body, GET_TODO_RESPONSE)

# integration/todo_app/test_list_todos.py
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
from tests.unit.todo_app.schemas import LIST_TODOS_RESPONSE
from tests.unit.todo_app.testutils import create_todo, list_todos


def test_list_todos(clear_todos: None) -> None:
    payload = {
        "name": TODO_NAME,
        "description": TODO_DESCRIPTION,
        "priority": TODO_PRIORITY,
    }
    create_todo(payload)

    assert len(list_todos()) == 1

    url = f"{API_PREFIX}/todos"
    response = requests.get(url)
    res_body = json.loads(response.text)

    assert response.status_code == HTTPStatus.OK
    assert len(res_body["todos"]) == 1
    assert res_body["todos"][0]["name"] == TODO_NAME
    assert res_body["todos"][0]["description"] == TODO_DESCRIPTION
    assert res_body["todos"][0]["priority"] == TODO_PRIORITY
    jsonschema.validate(res_body, LIST_TODOS_RESPONSE)

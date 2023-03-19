# todo_app/list_todos/test_integration.py
from http import HTTPStatus
import json
import os

import jsonschema
import requests

from tests.todo_app.schemas import LIST_TODOS_RESPONSE
from tests.todo_app.testutils import (
    TODO_DESCRIPTION,
    TODO_NAME,
    TODO_PRIORITY,
    create_todo,
    list_todos,
)


def test_list_todos(clear_todos: None) -> None:
    payload = {
        "name": TODO_NAME,
        "description": TODO_DESCRIPTION,
        "priority": TODO_PRIORITY,
    }
    create_todo(payload)

    assert len(list_todos()) == 1

    url = f"{os.environ['REST_API_URL']}/todos"
    response = requests.get(url)
    res_body = json.loads(response.text)

    assert response.status_code == HTTPStatus.OK
    assert len(res_body["todos"]) == 1
    assert res_body["todos"][0]["name"] == TODO_NAME
    assert res_body["todos"][0]["description"] == TODO_DESCRIPTION
    assert res_body["todos"][0]["priority"] == TODO_PRIORITY

    jsonschema.validate(res_body, LIST_TODOS_RESPONSE)

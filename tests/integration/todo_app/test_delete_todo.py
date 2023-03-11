# integration/todo_app/test_delete_todo.py
from http import HTTPStatus

import requests

from tests.integration.consts import API_PREFIX
from tests.unit.todo_app.consts import (
    TODO_DESCRIPTION,
    TODO_NAME,
    TODO_PRIORITY,
)
from tests.unit.todo_app.testutils import create_todo, list_todos


def test_delete_todo(clear_todos: None) -> None:
    payload = {
        "name": TODO_NAME,
        "description": TODO_DESCRIPTION,
        "priority": TODO_PRIORITY,
    }
    id = create_todo(payload)

    assert len(list_todos()) == 1

    url = f"{API_PREFIX}/todos/{id}"
    response = requests.delete(url)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert len(list_todos()) == 0

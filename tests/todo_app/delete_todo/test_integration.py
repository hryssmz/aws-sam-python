# todo_app/delete_todo/test_integration.py
from http import HTTPStatus
import os

import requests

from tests.todo_app.testutils import (
    TODO_DESCRIPTION,
    TODO_NAME,
    TODO_PRIORITY,
    create_todo,
    list_todos,
)


def test_delete_todo(clear_todos: None) -> None:
    payload = {
        "name": TODO_NAME,
        "description": TODO_DESCRIPTION,
        "priority": TODO_PRIORITY,
    }
    id = create_todo(payload)

    assert len(list_todos()) == 1

    url = f"{os.environ['REST_API_URL']}/todos/{id}"
    response = requests.delete(url)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert len(list_todos()) == 0

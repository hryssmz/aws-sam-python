# unit/todo_app/delete_todo/test_app.py
from http import HTTPStatus

from functions.todo_app.delete_todo import app
from tests.unit.testutils import get_dummy_apigw_event, get_dummy_context
from tests.unit.todo_app.consts import (
    TODO_DESCRIPTION,
    TODO_NAME,
    TODO_PRIORITY,
)
from tests.unit.todo_app.testutils import create_todo, list_todos


def test_no_content(clear_todos: None) -> None:
    payload = {
        "name": TODO_NAME,
        "description": TODO_DESCRIPTION,
        "priority": TODO_PRIORITY,
    }
    id = create_todo(payload)

    assert len(list_todos()) == 1

    event = get_dummy_apigw_event()
    event["pathParameters"] = {"id": id}
    context = get_dummy_context()
    response = app.handler(dict(event), context)

    assert response["statusCode"] == HTTPStatus.NO_CONTENT
    assert len(list_todos()) == 0

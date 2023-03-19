# todo_app/delete_todo/test_unit.py
from http import HTTPStatus

from pytest_mock import MockerFixture

from functions.todo_app.delete_todo import app
from tests.todo_app.testutils import (
    TODO_DESCRIPTION,
    TODO_NAME,
    TODO_PRIORITY,
    create_todo,
    get_dummy_apigw_event,
    get_dummy_context,
    get_test_logger,
    list_todos,
)

LOG_DIR = "reports/todo_app/log/delete_todo"


class TestNoContent:
    def test_1(self, clear_todos: None, mocker: MockerFixture) -> None:
        test_id = "TestNoContent.test_1"
        logger = get_test_logger(LOG_DIR, test_id)
        mocker.patch("logging.getLogger", return_value=logger)

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

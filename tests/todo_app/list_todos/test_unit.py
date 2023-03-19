# todo_app/list_todos/test_unit.py
from http import HTTPStatus
import json

import jsonschema
from pytest_mock import MockerFixture

from functions.todo_app.list_todos import app
from tests.todo_app.schemas import LIST_TODOS_RESPONSE
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

LOG_DIR = "reports/todo_app/log/list_todos"


class TestOK:
    def test_1(self, clear_todos: None, mocker: MockerFixture) -> None:
        test_id = "TestOk.test_1"
        logger = get_test_logger(LOG_DIR, test_id)
        mocker.patch("logging.getLogger", return_value=logger)

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

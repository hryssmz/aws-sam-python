# todo_app/update_todo/test_unit.py
from http import HTTPStatus
import json
import uuid

import jsonschema
from pytest_mock import MockerFixture

from functions.todo_app.update_todo import app
from tests.todo_app.schemas import CLIENT_ERROR, UPDATE_TODO_RESPONSE
from tests.todo_app.testutils import (
    TODO_DESCRIPTION,
    TODO_NAME,
    TODO_PRIORITY,
    create_todo,
    get_dummy_apigw_event,
    get_dummy_context,
    get_test_logger,
)

LOG_DIR = "reports/todo_app/log/update_todo"


class TestOK:
    def test_1(self, clear_todos: None, mocker: MockerFixture) -> None:
        test_id = "TestOk.test_1"
        logger = get_test_logger(LOG_DIR, test_id)
        mocker.patch("logging.getLogger", return_value=logger)

        id = create_todo({"name": "dummy", "description": "", "priority": 2})
        event = get_dummy_apigw_event()
        event["pathParameters"] = {"id": id}
        event["body"] = json.dumps(
            {
                "name": TODO_NAME,
                "description": TODO_DESCRIPTION,
                "priority": TODO_PRIORITY,
            }
        )
        context = get_dummy_context()
        response = app.handler(dict(event), context)
        res_body = json.loads(response["body"])

        assert response["statusCode"] == HTTPStatus.OK
        assert res_body["todo"]["id"] == id
        assert res_body["todo"]["name"] == TODO_NAME
        assert res_body["todo"]["description"] == TODO_DESCRIPTION
        assert res_body["todo"]["priority"] == TODO_PRIORITY

        jsonschema.validate(res_body, UPDATE_TODO_RESPONSE)


class TestBadRequest:
    def test_1(self, clear_todos: None, mocker: MockerFixture) -> None:
        test_id = "TestBadRequest.test_1"
        logger = get_test_logger(LOG_DIR, test_id)
        mocker.patch("logging.getLogger", return_value=logger)

        event = get_dummy_apigw_event()
        event["pathParameters"] = {"id": str(uuid.uuid4())}
        event["body"] = json.dumps(
            {
                "name": TODO_NAME,
                "description": TODO_DESCRIPTION,
                "priority": 5,
            }
        )
        context = get_dummy_context()
        response = app.handler(dict(event), context)
        res_body = json.loads(response["body"])

        assert response["statusCode"] == HTTPStatus.BAD_REQUEST

        jsonschema.validate(res_body, CLIENT_ERROR)


class TestNotFound:
    def test_1(self, clear_todos: None, mocker: MockerFixture) -> None:
        test_id = "TestNotFound.test_1"
        logger = get_test_logger(LOG_DIR, test_id)
        mocker.patch("logging.getLogger", return_value=logger)

        event = get_dummy_apigw_event()
        event["pathParameters"] = {"id": str(uuid.uuid4())}
        event["body"] = json.dumps(
            {
                "name": TODO_NAME,
                "description": TODO_DESCRIPTION,
                "priority": TODO_PRIORITY,
            }
        )
        context = get_dummy_context()
        response = app.handler(dict(event), context)
        res_body = json.loads(response["body"])

        assert response["statusCode"] == HTTPStatus.NOT_FOUND

        jsonschema.validate(res_body, CLIENT_ERROR)

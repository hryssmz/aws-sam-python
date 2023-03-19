# todo_app/create_todo/test_unit.py
from http import HTTPStatus
import json

import jsonschema
from pytest_mock import MockerFixture

from functions.todo_app.create_todo import app
from tests.todo_app.schemas import CLIENT_ERROR, CREATE_TODO_RESPONSE
from tests.todo_app.testutils import (
    TODO_DESCRIPTION,
    TODO_NAME,
    TODO_PRIORITY,
    get_dummy_apigw_event,
    get_dummy_context,
    get_test_logger,
    list_todos,
)

LOG_DIR = "reports/todo_app/log/create_todo"


class TestCreated:
    def test_1(self, clear_todos: None, mocker: MockerFixture) -> None:
        assert len(list_todos()) == 0

        test_id = "TestCreated.test_1"
        logger = get_test_logger(LOG_DIR, test_id)
        mocker.patch("logging.getLogger", return_value=logger)

        event = get_dummy_apigw_event()
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

        assert response["statusCode"] == HTTPStatus.CREATED
        assert len(list_todos()) == 1
        assert res_body["todo"]["name"] == TODO_NAME
        assert res_body["todo"]["description"] == TODO_DESCRIPTION
        assert res_body["todo"]["priority"] == TODO_PRIORITY

        jsonschema.validate(res_body, CREATE_TODO_RESPONSE)

    def test_2(self, clear_todos: None, mocker: MockerFixture) -> None:
        assert len(list_todos()) == 0

        test_id = "TestCreated.test_2"
        logger = get_test_logger(LOG_DIR, test_id)
        mocker.patch("logging.getLogger", return_value=logger)

        event = get_dummy_apigw_event()
        event["body"] = json.dumps({"name": TODO_NAME})
        context = get_dummy_context()
        response = app.handler(dict(event), context)
        res_body = json.loads(response["body"])

        assert response["statusCode"] == HTTPStatus.CREATED
        assert len(list_todos()) == 1
        assert res_body["todo"]["name"] == TODO_NAME
        assert res_body["todo"]["description"] == ""
        assert res_body["todo"]["priority"] == 2

        jsonschema.validate(res_body, CREATE_TODO_RESPONSE)


class TestBadRequest:
    def test_1(self, mocker: MockerFixture) -> None:
        test_id = "TestBadRequest.test_1"
        logger = get_test_logger(LOG_DIR, test_id)
        mocker.patch("logging.getLogger", return_value=logger)

        event = get_dummy_apigw_event()
        event["body"] = json.dumps({"description": TODO_DESCRIPTION})
        context = get_dummy_context()
        response = app.handler(dict(event), context)
        res_body = json.loads(response["body"])

        assert response["statusCode"] == HTTPStatus.BAD_REQUEST

        jsonschema.validate(res_body, CLIENT_ERROR)

    def test_2(self, mocker: MockerFixture) -> None:
        test_id = "TestBadRequest.test_2"
        logger = get_test_logger(LOG_DIR, test_id)
        mocker.patch("logging.getLogger", return_value=logger)

        event = get_dummy_apigw_event()
        event["body"] = json.dumps(
            {"name": TODO_NAME, "description": TODO_DESCRIPTION, "priority": 5}
        )
        context = get_dummy_context()
        response = app.handler(dict(event), context)
        res_body = json.loads(response["body"])

        assert response["statusCode"] == HTTPStatus.BAD_REQUEST

        jsonschema.validate(res_body, CLIENT_ERROR)

# s3_app/create_object/test_unit.py
from http import HTTPStatus
import json

import jsonschema
from pytest_mock import MockerFixture

from functions.s3_app.create_object import app
from tests.s3_app.schemas import CLIENT_ERROR, EMPTY_OBJECT
from tests.s3_app.testutils import (
    TEST_S3_BODY,
    TEST_S3_KEY,
    get_dummy_apigw_event,
    get_dummy_context,
    get_test_logger,
    list_objects,
)

LOG_DIR = "reports/s3_app/log/create_object"


class TestCreated:
    def test_1(self, clear_my_bucket: None, mocker: MockerFixture) -> None:
        test_id = "TestCreated.test_1"
        logger = get_test_logger(LOG_DIR, test_id)
        mocker.patch("logging.getLogger", return_value=logger)

        event = get_dummy_apigw_event()
        event["pathParameters"] = {"key": TEST_S3_KEY}
        event["body"] = json.dumps({"content": TEST_S3_BODY})
        context = get_dummy_context()
        response = app.handler(dict(event), context)
        res_body = json.loads(response["body"])

        assert response["statusCode"] == HTTPStatus.CREATED
        assert list_objects() == [TEST_S3_KEY]

        jsonschema.validate(res_body, EMPTY_OBJECT)


class TestBadRequest:
    def test_1(self, mocker: MockerFixture) -> None:
        test_id = "TestBadRequest.test_1"
        logger = get_test_logger(LOG_DIR, test_id)
        mocker.patch("logging.getLogger", return_value=logger)

        event = get_dummy_apigw_event()
        event["pathParameters"] = {"key": TEST_S3_KEY}
        event["body"] = json.dumps({})
        context = get_dummy_context()
        response = app.handler(dict(event), context)
        res_body = json.loads(response["body"])

        assert response["statusCode"] == HTTPStatus.BAD_REQUEST

        jsonschema.validate(res_body, CLIENT_ERROR)

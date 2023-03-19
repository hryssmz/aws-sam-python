# s3_app/get_object/test_unit.py
from http import HTTPStatus
import json

import jsonschema
from pytest_mock import MockerFixture

from functions.s3_app.get_object import app
from tests.s3_app.schemas import CLIENT_ERROR, GET_OBJECT_RESPONSE
from tests.s3_app.testutils import (
    TEST_S3_BODY,
    TEST_S3_KEY,
    get_dummy_apigw_event,
    get_dummy_context,
    get_my_bucket,
    get_test_logger,
)

LOG_DIR = "reports/s3_app/log/get_object"


class TestOk:
    def test_1(self, clear_my_bucket: None, mocker: MockerFixture) -> None:
        test_id = "TestOk.test_1"
        logger = get_test_logger(LOG_DIR, test_id)
        mocker.patch("logging.getLogger", return_value=logger)

        bucket = get_my_bucket()
        object = bucket.Object(TEST_S3_KEY)
        object.put(Body=TEST_S3_BODY.encode("utf-8"))

        event = get_dummy_apigw_event()
        event["pathParameters"] = {"key": TEST_S3_KEY}
        context = get_dummy_context()

        response = app.handler(dict(event), context)
        res_body = json.loads(response["body"])

        assert response["statusCode"] == HTTPStatus.OK
        assert res_body["content"] == TEST_S3_BODY

        jsonschema.validate(res_body, GET_OBJECT_RESPONSE)


class TestNotFound:
    def test_1(self, clear_my_bucket: None, mocker: MockerFixture) -> None:
        test_id = "TestNotFound.test_1"
        logger = get_test_logger(LOG_DIR, test_id)
        mocker.patch("logging.getLogger", return_value=logger)

        event = get_dummy_apigw_event()
        event["pathParameters"] = {"key": TEST_S3_KEY}
        context = get_dummy_context()
        response = app.handler(dict(event), context)
        res_body = json.loads(response["body"])

        assert response["statusCode"] == HTTPStatus.NOT_FOUND

        jsonschema.validate(res_body, CLIENT_ERROR)

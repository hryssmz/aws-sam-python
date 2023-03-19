# s3_app/delete_object/test_unit.py
from http import HTTPStatus

from pytest_mock import MockerFixture

from functions.s3_app.delete_object import app
from tests.s3_app.testutils import (
    TEST_S3_BODY,
    TEST_S3_KEY,
    get_dummy_apigw_event,
    get_dummy_context,
    get_my_bucket,
    get_test_logger,
    list_objects,
)

LOG_DIR = "reports/s3_app/log/delete_object"


class TestNoContent:
    def test_1(self, clear_my_bucket: None, mocker: MockerFixture) -> None:
        test_id = "TestNoContent.test_1"
        logger = get_test_logger(LOG_DIR, test_id)
        mocker.patch("logging.getLogger", return_value=logger)

        bucket = get_my_bucket()
        object = bucket.Object(TEST_S3_KEY)
        object.put(Body=TEST_S3_BODY.encode("utf-8"))

        assert list_objects() == [TEST_S3_KEY]

        event = get_dummy_apigw_event()
        event["pathParameters"] = {"key": TEST_S3_KEY}
        context = get_dummy_context()
        response = app.handler(dict(event), context)

        assert response["statusCode"] == HTTPStatus.NO_CONTENT
        assert list_objects() == []

        response = app.handler(dict(event), context)

        assert response["statusCode"] == HTTPStatus.NO_CONTENT

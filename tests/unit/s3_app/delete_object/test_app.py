# unit/s3_app/delete_object/test_app.py
from http import HTTPStatus

from functions.s3_app.delete_object import app
from tests.unit.s3_app.consts import TEST_S3_BODY, TEST_S3_KEY
from tests.unit.s3_app.testutils import get_my_bucket, list_objects
from tests.unit.testutils import get_dummy_apigw_event, get_dummy_context


def test_no_content(clear_my_bucket: None) -> None:
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

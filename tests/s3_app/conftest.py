# s3_app/conftest.py
import pytest

from tests.s3_app.testutils import get_my_bucket, list_objects


@pytest.fixture()
def clear_my_bucket() -> None:
    bucket = get_my_bucket()
    for key in list_objects():
        object = bucket.Object(key)
        object.delete()

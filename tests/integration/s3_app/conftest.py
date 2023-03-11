# integration/s3_app/conftest.py
import os

import pytest

from tests.unit.s3_app.testutils import get_my_bucket, list_objects

ENV_VARS = {
    "AWS_DEFAULT_REGION": "ap-northeast-1",
    "AWS_REGION": "ap-northeast-1",
    "MY_BUCKET": "aws-sam-python-mybucket-h6pgy39zwsuc",
}


@pytest.fixture(scope="session", autouse=True)
def env() -> None:
    for k, v in ENV_VARS.items():
        os.environ[k] = v


@pytest.fixture()
def clear_my_bucket() -> None:
    bucket = get_my_bucket()
    for key in list_objects():
        object = bucket.Object(key)
        object.delete()

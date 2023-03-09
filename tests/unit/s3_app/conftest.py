# unit/conftest.py
from typing import Generator

import boto3
import pytest

from tests.unit.s3_app.consts import TEST_BUCKET
from tests.unit.s3_app.testutils import list_buckets


@pytest.fixture()
def s3_fixture() -> Generator[None, None, None]:
    assert TEST_BUCKET not in list_buckets()

    yield

    if TEST_BUCKET in list_buckets():
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(TEST_BUCKET)
        for object_summary in bucket.objects.all():
            object = bucket.Object(object_summary.key)
            object.delete()

        bucket.delete()

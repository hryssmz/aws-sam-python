# unit/s3_app/testutils.py
import os
from typing import Any

import boto3


def get_my_bucket() -> Any:
    bucket_name = os.environ["MY_BUCKET"]
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)
    return bucket


def list_objects() -> list[str]:
    bucket = get_my_bucket()
    objects = [object.key for object in bucket.objects.all()]
    return objects

# unit/s3_app/testutils.py
import os
from typing import Any

import boto3


def create_bucket(bucket_name: str) -> Any:
    region = os.environ["AWS_REGION"]
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)
    bucket.create(CreateBucketConfiguration={"LocationConstraint": region})
    return bucket


def list_buckets() -> list[str]:
    client = boto3.client("s3")
    res = client.list_buckets()
    bucket_names = [bucket["Name"] for bucket in res["Buckets"]]
    return bucket_names


def list_objects(bucket_name: str) -> list[str]:
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)
    objects = [object.key for object in bucket.objects.all()]
    return objects

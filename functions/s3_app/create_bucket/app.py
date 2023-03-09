# s3_app/create_bucket/app.py
from http import HTTPStatus
import json
import os
from typing import Any

import boto3
from botocore.exceptions import ClientError
from utils import APIGW_RESPONSE, create_logger


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger = create_logger(context.function_name)
    logger.info("Event: " + json.dumps(event, ensure_ascii=False))

    bucket_name = event["pathParameters"]["bucket"]
    region = os.environ["AWS_REGION"]
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)

    try:
        bucket.create(CreateBucketConfiguration={"LocationConstraint": region})
        response = {
            **APIGW_RESPONSE,
            "statusCode": HTTPStatus.CREATED,
            "body": json.dumps({}),
        }
    except ClientError as exc:
        error = exc.response["Error"]
        if error["Code"] == "BucketAlreadyOwnedByYou":
            response = {
                **APIGW_RESPONSE,
                "statusCode": HTTPStatus.NO_CONTENT,
                "body": json.dumps(None),
            }
        elif error["Code"] == "BucketAlreadyExists":
            response = {
                **APIGW_RESPONSE,
                "statusCode": HTTPStatus.FORBIDDEN,
                "body": json.dumps(
                    {"code": error["Code"], "message": error["Message"]}
                ),
            }
        else:
            raise exc  # pragma: no cover

    return response

# s3_app/get_object/app.py
from http import HTTPStatus
import json
from typing import Any

import boto3
from botocore.exceptions import ClientError
from utils import APIGW_RESPONSE, create_logger


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger = create_logger(context.function_name)
    logger.info("Event: " + json.dumps(event, ensure_ascii=False))

    bucket_name = event["pathParameters"]["bucket"]
    key = event["pathParameters"]["key"]
    s3 = boto3.resource("s3")
    object = s3.Object(bucket_name, key)

    try:
        res = object.get()
        content = res["Body"].read().decode("utf-8")
        response = {
            **APIGW_RESPONSE,
            "statusCode": HTTPStatus.OK,
            "body": json.dumps({"content": content}),
        }
    except ClientError as exc:
        error = exc.response["Error"]
        if error["Code"] in ["NoSuchBucket", "NoSuchKey"]:
            response = {
                **APIGW_RESPONSE,
                "statusCode": HTTPStatus.NOT_FOUND,
                "body": json.dumps(
                    {"code": error["Code"], "message": error["Message"]}
                ),
            }
        elif error["Code"] == "AccessDenied":
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

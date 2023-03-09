# s3_app/create_object/app.py
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
    req_body = json.loads(event["body"])

    s3 = boto3.resource("s3")
    object = s3.Object(bucket_name, key)

    try:
        content: str = req_body["content"]
        object.put(Body=content.encode("utf-8"))
        response = {
            **APIGW_RESPONSE,
            "statusCode": HTTPStatus.CREATED,
            "body": json.dumps({}),
        }
    except KeyError as exc:
        response = {
            **APIGW_RESPONSE,
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": json.dumps({"code": "KeyError", "message": repr(exc)}),
        }
    except ClientError as exc:
        error = exc.response["Error"]
        if error["Code"] == "NoSuchBucket":
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

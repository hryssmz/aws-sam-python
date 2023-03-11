# s3_app/get_object/app.py
from http import HTTPStatus
import os
from typing import Any

import boto3
from botocore.exceptions import ClientError
from utils import APIGW_RESPONSE, create_logger, json_serialize


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger = create_logger(context.function_name)
    logger.info("Event: " + json_serialize(event))

    key = event["pathParameters"]["key"]
    s3 = boto3.resource("s3")
    object = s3.Object(os.environ["MY_BUCKET"], key)

    try:
        res = object.get()
    except ClientError as exc:
        error = exc.response["Error"]
        if error["Code"] == "NoSuchKey":
            response = {
                **APIGW_RESPONSE,
                "statusCode": HTTPStatus.NOT_FOUND,
                "body": json_serialize(
                    {"code": error["Code"], "message": error["Message"]}
                ),
            }
            return response
        else:
            raise exc  # pragma: no cover

    content = res["Body"].read().decode("utf-8")
    response = {
        **APIGW_RESPONSE,
        "statusCode": HTTPStatus.OK,
        "body": json_serialize({"content": content}),
    }

    return response

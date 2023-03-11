# s3_app/delete_object/app.py
from http import HTTPStatus
import os
from typing import Any

import boto3
from utils import APIGW_RESPONSE, create_logger, json_serialize


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger = create_logger(context.function_name)
    logger.info("Event: " + json_serialize(event))

    key = event["pathParameters"]["key"]
    s3 = boto3.resource("s3")
    object = s3.Object(os.environ["MY_BUCKET"], key)
    object.delete()
    response = {
        **APIGW_RESPONSE,
        "statusCode": HTTPStatus.NO_CONTENT,
        "body": json_serialize(None),
    }

    return response

# s3_app/create_object/app.py
from http import HTTPStatus
import json
import os
from typing import Any

import boto3
import jsonschema
from utils import APIGW_RESPONSE, create_logger, json_serialize

PUT_OBJECT_REQUEST = {
    "type": "object",
    "required": ["content"],
    "properties": {"content": {"type": "string"}},
}


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger = create_logger(context.function_name)
    logger.info("Event: " + json_serialize(event))

    key = event["pathParameters"]["key"]
    req_body = json.loads(event["body"])

    try:
        jsonschema.validate(req_body, PUT_OBJECT_REQUEST)
    except jsonschema.ValidationError as exc:
        response = {
            **APIGW_RESPONSE,
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": json_serialize(
                {"code": "ValidationError", "message": exc.message}
            ),
        }
        return response

    s3 = boto3.resource("s3")
    object = s3.Object(os.environ["MY_BUCKET"], key)
    content: str = req_body["content"]
    object.put(Body=content.encode("utf-8"))
    response = {
        **APIGW_RESPONSE,
        "statusCode": HTTPStatus.CREATED,
        "body": json_serialize({}),
    }

    return response

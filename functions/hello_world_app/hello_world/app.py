# hello_world_app/hello_world/app.py
from http import HTTPStatus
from typing import Any

from utils import APIGW_RESPONSE, create_logger, json_serialize


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger = create_logger(context.function_name)
    logger.info("Event: " + json_serialize(event))

    response = {
        **APIGW_RESPONSE,
        "statusCode": HTTPStatus.BAD_REQUEST,
        "body": json_serialize({"message": "Hello World!"}),
    }
    return response

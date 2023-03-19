# todo_app/list_todos/app.py
from http import HTTPStatus
import json
import os
from typing import Any

import boto3
from utils import APIGW_RESPONSE, create_logger, json_serialize


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger = create_logger(context.function_name)
    logger.info("Event: " + json_serialize(event))

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["TODO_TABLE"])
    result = table.scan()

    response = {
        **APIGW_RESPONSE,
        "statusCode": HTTPStatus.OK,
        "body": dynamodb_serialize({"todos": result["Items"]}),
    }
    return response


class DynamoDBEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        return float(obj)


def dynamodb_serialize(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, cls=DynamoDBEncoder)

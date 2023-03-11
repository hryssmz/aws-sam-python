# todo_app/get_todo/app.py
from http import HTTPStatus
import json
import os
from typing import Any

import boto3
from utils import APIGW_RESPONSE, create_logger, json_serialize


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger = create_logger(context.function_name)
    logger.info("Event: " + json_serialize(event))

    path_params: dict[str, str] = event["pathParameters"]
    table_name = os.environ["TODO_TABLE"]
    key = {"id": path_params["id"]}

    try:
        todo = get_item(table_name, key)
    except KeyError:
        response = {
            **APIGW_RESPONSE,
            "statusCode": HTTPStatus.NOT_FOUND,
            "body": json_serialize(
                {"code": "NonExistKey", "message": dynamodb_serialize(key)}
            ),
        }
        return response

    response = {
        **APIGW_RESPONSE,
        "statusCode": HTTPStatus.OK,
        "body": json_serialize({"todo": todo}),
    }
    return response


def get_item(table_name: str, key: dict[str, Any]) -> dict[str, Any]:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    result = table.get_item(Key=key)
    item: dict[str, Any] = dynamodb_convert(result["Item"])
    return item


class DynamoDBEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        return float(obj)


def dynamodb_serialize(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, cls=DynamoDBEncoder)


def dynamodb_convert(obj: Any) -> Any:
    return json.loads(dynamodb_serialize(obj))

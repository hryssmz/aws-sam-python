# todo_app/delete_todo/app.py
from http import HTTPStatus
import os
from typing import Any

import boto3
from utils import APIGW_RESPONSE, create_logger, json_serialize


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger = create_logger(context.function_name)
    logger.info("Event: " + json_serialize(event))

    path_params = event["pathParameters"]

    table_name = os.environ["TODO_TABLE"]
    key = {"id": path_params["id"]}
    delete_item(table_name, key)

    response = {
        **APIGW_RESPONSE,
        "statusCode": HTTPStatus.NO_CONTENT,
        "body": json_serialize(None),
    }
    return response


def delete_item(table_name: str, key: dict[str, Any]) -> None:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    table.delete_item(Key=key)

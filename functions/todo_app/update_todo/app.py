# todo_app/update_todo/app.py
from datetime import datetime
from http import HTTPStatus
import json
import os
from typing import Any

import boto3
import jsonschema
from utils import APIGW_RESPONSE, create_logger, json_serialize

UPDATE_TODO_REQUEST = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "priority": {"type": "integer", "minimum": 1, "maximum": 3},
    },
}


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger = create_logger(context.function_name)
    logger.info("Event: " + json_serialize(event))

    path_params: dict[str, str] = event["pathParameters"]
    req_body: dict[str, Any] = json.loads(event["body"])

    try:
        jsonschema.validate(req_body, UPDATE_TODO_REQUEST)
    except jsonschema.ValidationError as exc:
        response = {
            **APIGW_RESPONSE,
            "statusCode": HTTPStatus.BAD_REQUEST,
            "body": json_serialize(
                {"code": "ValidationError", "message": exc.message}
            ),
        }
        return response

    table_name = os.environ["TODO_TABLE"]
    key = {"id": path_params["id"]}

    try:
        get_item(table_name, key)
    except KeyError:
        response = {
            **APIGW_RESPONSE,
            "statusCode": HTTPStatus.NOT_FOUND,
            "body": json_serialize(
                {"code": "NonExistKey", "message": dynamodb_serialize(key)}
            ),
        }
        return response

    todo = update_item(table_name, key, req_body)
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


def update_item(
    table_name: str, key: dict[str, Any], payload: dict[str, Any]
) -> dict[str, Any]:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    payload.update({"updatedAt": format_date(datetime.utcnow())})
    expr = "SET " + ", ".join([f"#{k} = :{k}" for k in payload.keys()])
    expr_names = {f"#{k}": k for k in payload.keys()}
    expr_values = {f":{k}": v for k, v in payload.items()}

    result = table.update_item(
        Key=key,
        UpdateExpression=expr,
        ExpressionAttributeNames=expr_names,
        ExpressionAttributeValues=expr_values,
        ReturnValues="ALL_NEW",
    )
    item: dict[str, Any] = dynamodb_convert(result["Attributes"])
    return item


def format_date(dt: datetime, fmt: str = "%Y-%m-%dT%H:%M:%SZ") -> str:
    return datetime.strftime(dt, fmt)


class DynamoDBEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        return float(obj)


def dynamodb_serialize(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, cls=DynamoDBEncoder)


def dynamodb_convert(obj: Any) -> Any:
    return json.loads(dynamodb_serialize(obj))

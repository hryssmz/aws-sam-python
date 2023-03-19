# todo_app/create_todo/app.py
from datetime import datetime
from http import HTTPStatus
import json
import os
from typing import Any
import uuid

import boto3
import jsonschema
from utils import APIGW_RESPONSE, create_logger, json_serialize

CREATE_TODO_REQUEST = {
    "type": "object",
    "required": ["name"],
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "priority": {"type": "integer", "minimum": 1, "maximum": 3},
    },
}


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger = create_logger(context.function_name)
    logger.info("Event: " + json_serialize(event))

    req_body: dict[str, Any] = json.loads(event["body"])

    try:
        jsonschema.validate(req_body, CREATE_TODO_REQUEST)
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
    payload = {
        "name": req_body["name"],
        "description": req_body.get("description", ""),
        "priority": req_body.get("priority", 2),
    }
    todo = put_item(table_name, payload)

    response = {
        **APIGW_RESPONSE,
        "statusCode": HTTPStatus.CREATED,
        "body": json_serialize({"todo": todo}),
    }

    return response


def put_item(table_name: str, payload: dict[str, Any]) -> dict[str, Any]:
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    id = str(uuid.uuid4())
    item = {
        **payload,
        "id": id,
        "createdAt": format_date(datetime.utcnow()),
        "updatedAt": format_date(datetime.utcnow()),
    }
    table.put_item(Item=item)
    return item


def format_date(dt: datetime, fmt: str = "%Y-%m-%dT%H:%M:%SZ") -> str:
    return datetime.strftime(dt, fmt)

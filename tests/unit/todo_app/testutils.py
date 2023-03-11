# unit/todo_app/conftest.py
from datetime import datetime
import os
from typing import Any
import uuid

import boto3


def get_todo_table() -> Any:
    dynamodb = boto3.resource("dynamodb")
    todo_table = dynamodb.Table(os.environ["TODO_TABLE"])
    return todo_table


def list_todos() -> list[dict[str, Any]]:
    todo_table = get_todo_table()
    result = todo_table.scan()
    todos: list[dict[str, Any]] = result["Items"]
    return todos


def create_todo(payload: dict[str, Any]) -> str:
    todo_table = get_todo_table()
    id = str(uuid.uuid4())
    item = {
        **payload,
        "id": id,
        "createdAt": format_date(datetime.utcnow()),
        "updatedAt": format_date(datetime.utcnow()),
    }
    todo_table.put_item(Item=item)
    return id


def format_date(dt: datetime, fmt: str = "%Y-%m-%dT%H:%M:%SZ") -> str:
    return datetime.strftime(dt, fmt)

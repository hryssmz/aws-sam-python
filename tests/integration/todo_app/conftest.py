# integration/todo_app/conftest.py
import os

import pytest

from tests.unit.todo_app.testutils import get_todo_table, list_todos

ENV_VARS = {
    "AWS_DEFAULT_REGION": "ap-northeast-1",
    "AWS_REGION": "ap-northeast-1",
    "TODO_TABLE": "aws-sam-python-TodoTable-1D0RU3EQUY48W",
}


@pytest.fixture(scope="session", autouse=True)
def env() -> None:
    for k, v in ENV_VARS.items():
        os.environ[k] = v


@pytest.fixture()
def clear_todos() -> None:
    todo_table = get_todo_table()
    for todo in list_todos():
        todo_table.delete_item(Key={"id": todo["id"]})

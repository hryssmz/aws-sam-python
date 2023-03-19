# todo_app/conftest.py
import pytest

from tests.todo_app.testutils import get_todo_table, list_todos


@pytest.fixture()
def clear_todos() -> None:
    todo_table = get_todo_table()
    for todo in list_todos():
        todo_table.delete_item(Key={"id": todo["id"]})

#!/bin/sh
pytest_lambda() {
    pytest \
        --cov-report=term \
        --cov-report="html:tests/unit/$1/htmlcov" \
        --cov="functions/$1" \
        --override-ini="pythonpath=functions/$1 ." \
        "tests/unit/$1" || exit 1
}

pytest_hello_world_app() {
    pytest_lambda hello_world_app/hello_world
}

pytest_s3_app() {
    pytest_lambda s3_app/list_objects
    pytest_lambda s3_app/create_object
    pytest_lambda s3_app/get_object
    pytest_lambda s3_app/delete_object
}

pytest_todo_app() {
    pytest_lambda todo_app/list_todos
    pytest_lambda todo_app/create_todo
    pytest_lambda todo_app/delete_todo
    pytest_lambda todo_app/update_todo
    pytest_lambda todo_app/get_todo
}

pytest_hello_world_app
# pytest_s3_app
# pytest_todo_app

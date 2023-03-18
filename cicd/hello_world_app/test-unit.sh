#!/bin/sh
pytest_lambda() {
    pytest \
        --cov-report=term \
        --cov-report="html:htmlcov" \
        --cov-report="xml:coverage.xml" \
        --cov="functions/$1" \
        --override-ini="pythonpath=functions/$1 ." \
        "tests/unit/$1"
}

pytest_hello_world_app() {
    pytest_lambda hello_world_app/hello_world
}

pytest_hello_world_app

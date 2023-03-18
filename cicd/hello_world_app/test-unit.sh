#!/bin/sh
pytest_lambda() {
    pytest \
        --cov-report=term \
        --cov-report="html:tests/report/htmlcov/$1" \
        --cov-report="xml:tests/report/clover/$1.xml" \
        --cov="functions/$1" \
        --override-ini="pythonpath=functions/$1 ." \
        --junitxml="tests/report/junit/$1.xml" \
        "tests/unit/$1"
}

pytest_hello_world_app() {
    pytest_lambda hello_world_app/hello_world
}

pytest_hello_world_app

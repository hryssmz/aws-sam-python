#!/bin/sh
pytest_lambda() {
    pytest \
        --cov-report=term \
        --cov-report="html:tests/$1/report/htmlcov/$2" \
        --cov-report="xml:tests/$1/report/clover/$2.xml" \
        --cov="functions/$1/$2" \
        --override-ini="pythonpath=functions/$1/$2 ." \
        --junitxml="tests/$1/report/junit/$2.xml" \
        "tests/$1/$2/test_unit.py"
}

pytest_hello_world_app() {
    pytest_lambda hello_world_app hello_world
}

pytest_hello_world_app

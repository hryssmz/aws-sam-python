#!/bin/sh
pytest_lambda() {
    mkdir -p "tests/$1/report/log/$2"
    pytest \
        --override-ini="pythonpath=functions/$1/$2 ." \
        --log-file-level=INFO \
        --log-file="tests/$1/report/log/$2/test_unit.log" \
        --junitxml="tests/$1/report/junit/$2.xml" \
        --cov-report=term \
        --cov-report="html:tests/$1/report/htmlcov/$2" \
        --cov-report="xml:tests/$1/report/clover/$2.xml" \
        --cov="functions/$1/$2" \
        "tests/$1/$2/test_unit.py" |
            tee "tests/$1/report/log/$2/pytest.log"
}

pytest_hello_world_app() {
    pytest_lambda hello_world_app hello_world
}

pytest_hello_world_app

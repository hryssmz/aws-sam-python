#!/bin/sh
APP_NAME="hello_world_app"

mkdir -p "tests/${APP_NAME}/report/log/$1"
pytest \
    --override-ini="pythonpath=functions/${APP_NAME}/$1 ." \
    --log-file-level=INFO \
    --log-file="tests/${APP_NAME}/report/log/$1.log" \
    --junitxml="tests/${APP_NAME}/report/junit/$1.xml" \
    --cov-report=term \
    --cov-report="html:tests/${APP_NAME}/report/htmlcov/$1" \
    --cov-report="xml:tests/${APP_NAME}/report/cobertura/$1.xml" \
    --cov="functions/${APP_NAME}/$1" \
    "tests/${APP_NAME}/$1/test_unit.py"

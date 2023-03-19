#!/bin/sh
pytest \
    --override-ini="pythonpath=functions/${APP_NAME}/$1 ." \
    --junitxml="reports/${APP_NAME}/junit/$1.xml" \
    --cov-report=term \
    --cov-report="html:reports/${APP_NAME}/htmlcov/$1" \
    --cov-report="xml:reports/${APP_NAME}/cobertura/$1.xml" \
    --cov="functions/${APP_NAME}/$1" \
    "tests/${APP_NAME}/$1/test_unit.py"

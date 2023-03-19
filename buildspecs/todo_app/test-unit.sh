#!/bin/sh
pytest \
    --override-ini="pythonpath=functions/${APP_NAME}/$1 ." \
    --junitxml="reports/${APP_NAME}/junit/$1.xml" \
    --cov-append \
    --cov-report=term \
    --cov-report="html:reports/${APP_NAME}/htmlcov" \
    --cov-report="xml:reports/${APP_NAME}/coverage.xml" \
    --cov="functions/${APP_NAME}/$1" \
    "tests/${APP_NAME}/$1/test_unit.py"

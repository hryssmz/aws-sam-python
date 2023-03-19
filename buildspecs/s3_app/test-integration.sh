#!/bin/sh
pytest \
    --junitxml="reports/${APP_NAME}/junit/$1.xml" \
    "tests/${APP_NAME}/$1/test_integration.py"

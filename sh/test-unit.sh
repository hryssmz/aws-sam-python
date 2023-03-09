#!/bin/sh
pytest_lambda() {
    pytest \
        --cov-report=term \
        --cov-report="html:tests/unit/$1/htmlcov" \
        --cov="functions/$1" \
        --override-ini="pythonpath=functions/$1 ." \
        "tests/unit/$1" || exit 1
}

pytest_s3_app() {
    pytest_lambda s3_app/list_buckets
    pytest_lambda s3_app/create_bucket
    pytest_lambda s3_app/delete_bucket
    pytest_lambda s3_app/list_objects
    pytest_lambda s3_app/create_object
    pytest_lambda s3_app/get_object
    pytest_lambda s3_app/delete_object
}

pytest_s3_app

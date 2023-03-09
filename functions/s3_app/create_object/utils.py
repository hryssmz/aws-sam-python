# s3_app/create_object/utils.py
from http import HTTPStatus
import json
import logging

APIGW_RESPONSE = {
    "statusCode": HTTPStatus.OK,
    "headers": {"Access-Control-Allow-Origin": "*"},
    "body": json.dumps({}),
    "multiValueHeaders": {},
    "isBase64Encoded": False,
}


def create_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger

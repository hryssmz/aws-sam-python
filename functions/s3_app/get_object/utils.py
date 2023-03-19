# s3_app/get_object/utils.py
from http import HTTPStatus
import json
import logging
from typing import Any

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


def json_serialize(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False)

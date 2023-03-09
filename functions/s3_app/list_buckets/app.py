# s3_app/list_buckets/app.py
from http import HTTPStatus
import json
from typing import Any

import boto3
from utils import APIGW_RESPONSE, create_logger


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger = create_logger(context.function_name)
    logger.info("Event: " + json.dumps(event, ensure_ascii=False))

    client = boto3.client("s3")
    res = client.list_buckets()
    bucket_names = [bucket["Name"] for bucket in res["Buckets"]]

    response = {
        **APIGW_RESPONSE,
        "statusCode": HTTPStatus.OK,
        "body": json.dumps({"buckets": bucket_names}),
    }
    return response

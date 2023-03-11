# s3_app/list_objects/app.py
from http import HTTPStatus
import os
from typing import Any

import boto3
from utils import APIGW_RESPONSE, create_logger, json_serialize


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    logger = create_logger(context.function_name)
    logger.info("Event: " + json_serialize(event))

    s3 = boto3.resource("s3")
    bucket = s3.Bucket(os.environ["MY_BUCKET"])
    objects = [object.key for object in bucket.objects.all()]
    response = {
        **APIGW_RESPONSE,
        "statusCode": HTTPStatus.OK,
        "body": json_serialize({"objects": objects}),
    }

    return response

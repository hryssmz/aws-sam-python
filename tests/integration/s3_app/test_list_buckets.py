# integration/s3_app/test_list_buckets.py
from http import HTTPStatus
import json

import jsonschema
import requests

from tests.integration.consts import API_PREFIX
from tests.unit.schemas import GET_BUCKETS_RESPONSE


def test_list_buckets() -> None:
    url = f"{API_PREFIX}/buckets"
    response = requests.get(url)

    assert response.status_code == HTTPStatus.OK
    jsonschema.validate(json.loads(response.text), GET_BUCKETS_RESPONSE)

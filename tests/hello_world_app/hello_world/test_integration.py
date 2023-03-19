# hello_world_app/hello_world/test_integration.py
from http import HTTPStatus
import json
import os

import jsonschema
import requests

from tests.hello_world_app.schemas import HELLO_WORLD_RESPONSE


def test_create_object() -> None:
    url = f"{os.environ['REST_API_URL']}/"
    response = requests.get(url)
    res_body = json.loads(response.text)

    assert response.status_code == HTTPStatus.OK
    assert res_body["message"] == "Hello World!"

    jsonschema.validate(res_body, HELLO_WORLD_RESPONSE)

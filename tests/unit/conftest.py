# unit/conftest.py
import os

import pytest

ENV_VARS = {
    "AWS_DEFAULT_REGION": "ap-northeast-1",
    "AWS_REGION": "ap-northeast-1",
}


@pytest.fixture(scope="session", autouse=True)
def env() -> None:
    for k, v in ENV_VARS.items():
        os.environ[k] = v

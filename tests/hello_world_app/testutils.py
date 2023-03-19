# hello_world_app/testutils.py
import json

from aws_lambda_typing.context import Client, ClientContext, Context, Identity
from aws_lambda_typing.events import APIGatewayProxyEventV1


def get_dummy_apigw_event() -> APIGatewayProxyEventV1:
    return APIGatewayProxyEventV1(
        body=json.dumps({"message": "hello world"}),
        headers={
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/webp,*/*;q=0.8"
            ),
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "en-US,en;q=0.8",
            "Cache-Control": "max-age=0",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-Mobile-Viewer": "false",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Tablet-Viewer": "false",
            "CloudFront-Viewer-Country": "US",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Custom User Agent String",
            "Via": (
                "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net "
                "(CloudFront)"
            ),
            "X-Amz-Cf-Id": (
                "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA=="
            ),
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https",
        },
        httpMethod="GET",
        isBase64Encoded=False,
        multiValueHeaders={},
        multiValueQueryStringParameters={},
        path="/hello",
        pathParameters={"proxy": "/path/to/resource"},
        queryStringParameters={"foo": "bar"},
        requestContext={
            "accountId": "123456789012",
            "resourceId": "123456",
            "stage": "prod",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "requestTime": "09/Apr/2015:12:34:56 +0000",
            "requestTimeEpoch": 1428582896000,
            "identity": {
                "cognitoIdentityPoolId": None,
                "accountId": None,
                "cognitoIdentityId": None,
                "caller": None,
                "accessKey": None,
                "sourceIp": "127.0.0.1",
                "cognitoAuthenticationType": None,
                "cognitoAuthenticationProvider": None,
                "userArn": None,
                "userAgent": "Custom User Agent String",
                "user": None,
            },
            "path": "/prod/hello",
            "resourcePath": "/hello",
            "httpMethod": "POST",
            "apiId": "1234567890",
            "protocol": "HTTP/1.1",
        },
        resource="/hello",
        stageVariables={"baz": "qux"},
    )


def get_dummy_context() -> Context:
    context = Context()
    context.aws_request_id = "aws_request_id"
    context.client_context = ClientContext(
        client=Client(
            app_package_name="app_package_name",
            app_title="app_title",
            app_version_code="app_version_code",
            app_version_name="app_version_name",
            installation_id="installation_id",
        ),
        custom={"key": "val"},
        env={"key": "val"},
    )
    context.function_name = "function_name"
    context.function_version = "function_version"
    context.identity = Identity(
        cognito_identity_id="cognito_identity_id",
        cognito_identity_pool_id="cognito_identity_pool_id",
    )
    context.invoked_function_arn = "invoked_function_arn"
    context.log_group_name = "log_group_name"
    context.log_stream_name = "log_stream_name"
    context.memory_limit_in_mb = "memory_limit_in_mb"
    return context

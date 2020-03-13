from typing import Collection, Dict, Union

import pytest

import os
import uuid

from app.app import dynamodb


IdentifyType = Collection[str]
# IdentifyType = Dict[str, str]
RequestContextType = Dict[str, Union[str, IdentifyType]]

QueryStringParametersType = Dict[str, str]
HeadersType = Dict[str, str]
PathParametersType = Dict[str, str]
StageVariablesType = Dict[str, str]

ApiGatewayEventType = Dict[
    str, Union[
        str,
        RequestContextType,
        QueryStringParametersType,
        HeadersType,
        PathParametersType,
        StageVariablesType,
    ]
]


@pytest.fixture()
def apigw_event() -> ApiGatewayEventType:
    """ Generates API GW Event"""

    return {
        "body": '{ "test": "body"}',
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": "",
            },
            "stage": "prod",
        },
        "queryStringParameters": {"foo": "bar"},
        "headers": {
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch",
        },
        "pathParameters": {"proxy": "/examplepath"},
        "httpMethod": "POST",
        "stageVariables": {"baz": "qux"},
        "path": "/examplepath",
    }


@pytest.fixture(autouse=True)
# TODO: Specify appropriate return type
def fx_dynamodb_table():  # type: ignore
    table = dynamodb.create_table(
        TableName=os.environ['DYNAMODB_TABLE_NAME'],
        KeySchema=[
            {
                'AttributeName': 'user_id',
                'KeyType': 'HASH',
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'user_id',
                'AttributeType': 'S',
            },
        ],
        BillingMode='PAY_PER_REQUEST',
    )
    yield table
    table.delete()


@pytest.fixture
# TODO: Specify appropriate return type
def fx_dummy_user(fx_dynamodb_table):
    user = {'user_id': uuid.uuid4().hex, 'name': 'fatsushi'}
    fx_dynamodb_table.put_item(Item=user)
    yield user
    fx_dynamodb_table.delete_item(Key={'user_id': user['user_id']})

from typing import Any, Dict, Union

import boto3

import json


dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:8000',  # TODO: Refer env var or something instead
)
table = dynamodb.Table('testUserTable')  # TODO: Refer env var or something instead

EventType = Dict[str, Any]
ContextType = Dict[str, Any]
ResponseType = Dict[str, Union[str, int]]


def lambda_handler(event: EventType, context: ContextType) -> ResponseType:
    result = table.scan()
    return {
        'statusCode': 200,
        'body': json.dumps(result),
    }

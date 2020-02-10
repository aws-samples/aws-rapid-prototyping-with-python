import json

import pytest

from app import app


def test_lambda_handler(apigw_event, mocker):

    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert data['Count'] == 0
    assert data['Items'] == []

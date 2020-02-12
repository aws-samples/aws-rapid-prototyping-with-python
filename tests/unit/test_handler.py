import json
from http import HTTPStatus

import pytest

from app import app


class TestDispatchRequestGet:
    @pytest.fixture
    def event(self, apigw_event, fx_dummy_user):  # TODO: Specify type
        apigw_event['requestContext']['path'] = '/user/{user_id}'
        apigw_event['httpMethod'] = 'GET'
        apigw_event['pathParameters']['user_id'] = fx_dummy_user['user_id']
        return apigw_event

    def test_200(self, event, fx_dummy_user) -> None:
        response = app.dispatch_request(event, {})
        assert response['statusCode'] == HTTPStatus.OK
        assert json.loads(response['body']) == fx_dummy_user

    def test_404(self, event) -> None:
        event['pathParameters']['user_id'] = 'DUMMYID'

        response = app.dispatch_request(event, {})
        assert response['statusCode'] == HTTPStatus.NOT_FOUND

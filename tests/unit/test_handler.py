import json
from http import HTTPStatus

import pytest

from app import app


class TestDispatchRequestGeneral:
    def test_404(self, apigw_event) -> None:
        apigw_event['requestContext']['path'] = '/NOT_IMPLEMENTED_PATH'
        response = app.dispatch_request(apigw_event, {})
        assert response['statusCode'] == HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize('not_allowed_method', (
        'POST', 'OPTIONS', 'CONNECT', 'TRACE',
    ))
    def test_405(self, apigw_event, not_allowed_method: str) -> None:
        apigw_event['requestContext']['path'] = '/user'
        apigw_event['httpMethod'] = not_allowed_method
        response = app.dispatch_request(apigw_event, {})
        assert response['statusCode'] == HTTPStatus.METHOD_NOT_ALLOWED


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


class TestDispatchRequestPut:
    @pytest.fixture
    def event(self, apigw_event):  # TODO: Specify type
        apigw_event['requestContext']['path'] = '/user'
        apigw_event['httpMethod'] = 'PUT'
        apigw_event['body'] = json.dumps({'name': 'fatsushi'})
        return apigw_event

    def test_200(self, event, fx_dynamodb_table) -> None:
        response = app.dispatch_request(event, {})
        response_json = json.loads(response['body'])
        assert response['statusCode'] == HTTPStatus.CREATED
        assert fx_dynamodb_table.scan()['Items'][0] == response_json

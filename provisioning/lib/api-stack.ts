import * as cdk from '@aws-cdk/core';
import * as lambda from '@aws-cdk/aws-lambda';
import * as apigateway from '@aws-cdk/aws-apigateway';
import { DatabaseStack } from './database-stack';

export interface ApiStackProps {
    database: DatabaseStack,
}

export class ApiStack extends cdk.Stack {
    constructor(scope: cdk.Construct, id: string, apiProps: ApiStackProps, props?: cdk.StackProps) {
        super(scope, id, props);

        const userFunction = new lambda.Function(this, 'UserFunction', {
            runtime: lambda.Runtime.PYTHON_3_8,
            code: lambda.Code.asset('../app'),
            environment: {
                DYNAMODB_TABLE_NAME: apiProps.database.table.tableName,
            },
            functionName: 'UserFunction',
            handler: 'app.dispatch_request',
        });
        
        apiProps.database.table.grantReadWriteData(userFunction);

        const userFunctionIntegration = new apigateway.LambdaIntegration(userFunction, {});

        const api = new apigateway.RestApi(this, 'UserRestApi', { restApiName: 'userRestApi' });
        const apiUser = api.root.addResource('user');
        const apiUserId = apiUser.addResource('{user_id}');

        apiUser.addMethod('PUT', userFunctionIntegration);
        apiUserId.addMethod('GET', userFunctionIntegration);
        apiUserId.addMethod('DELETE', userFunctionIntegration);
        apiUserId.addMethod('PATCH', userFunctionIntegration);
    }
}

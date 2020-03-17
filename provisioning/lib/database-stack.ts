import * as cdk from '@aws-cdk/core';
import * as dynamodb from '@aws-cdk/aws-dynamodb';

export class DatabaseStack extends cdk.Stack {
    public readonly table: dynamodb.Table;

    constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        this.table = new dynamodb.Table(this, 'UserTable', {
            tableName: 'UserTable',
            partitionKey: {
                name: 'user_id',
                type: dynamodb.AttributeType.STRING,
            },
            sortKey: {
                name: 'name',
                type: dynamodb.AttributeType.STRING,
            },
        });
    }
}

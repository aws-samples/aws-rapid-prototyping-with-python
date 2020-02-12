import * as cdk from '@aws-cdk/core';
import * as dynamodb from '@aws-cdk/aws-dynamodb';

export class ProvisioningStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    new dynamodb.Table(this, 'userTable', {
      partitionKey: {
        name: 'id',
        type: dynamodb.AttributeType.STRING,
      },
      sortKey: {
        name: 'name',
        type: dynamodb.AttributeType.STRING,
      },
    });
  }
}

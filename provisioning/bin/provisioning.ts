#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { ProvisioningStack } from '../lib/provisioning-stack';

const app = new cdk.App();
new ProvisioningStack(app, 'ProvisioningStack');

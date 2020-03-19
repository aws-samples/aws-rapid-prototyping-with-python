#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { DatabaseStack } from '../lib/database-stack';
import { ApiStack } from '../lib/api-stack';

const app = new cdk.App();
const db = new DatabaseStack(app, 'DatabaseStack');
const api = new ApiStack(app, 'ApiStack', { database: db });

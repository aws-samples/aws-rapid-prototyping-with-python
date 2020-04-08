#!/bin/bash
set -e

CWD=$(dirname "${0}")
DOCKER_NETWORK_NAME=lambda-local
DDB_TABLE_NAME=testUserTable
DDB_CONTAINER_PREFIX=dynamodblocalpythonrapid
DDB_CONTAINER_NAME=${DDB_CONTAINER_PREFIX}$(date "+%Y%m%d%H%M%S")
DDB_LOCAL_PORT=8001
EXISTING_CONTAINERS=$(docker ps -aq --filter name=${DDB_CONTAINER_PREFIX})
PATH_TO_ENVVAR=/tmp/pythonrapidenv.json

docker pull amazon/dynamodb-local

# Create a docker network common between DDB Local and SAM Local
if docker network ls | grep ${DOCKER_NETWORK_NAME}; then
  echo
else
  docker network create ${DOCKER_NETWORK_NAME}
fi

# Lanuch DDB Local
if [ ! "x${EXISTING_CONTAINERS}" = "x" ]; then
  docker stop ${EXISTING_CONTAINERS}
  docker rm ${EXISTING_CONTAINERS}
fi
docker run -d --name ${DDB_CONTAINER_NAME} --net ${DOCKER_NETWORK_NAME} -p ${DDB_LOCAL_PORT}:8000 amazon/dynamodb-local

# Create DDB schema
/usr/local/bin/aws dynamodb create-table --endpoint-url http://localhost:${DDB_LOCAL_PORT} \
  --table-name ${DDB_TABLE_NAME} \
  --attribute-definitions AttributeName=user_id,AttributeType=S \
  --key-schema AttributeName=user_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# Launch SAM Local
echo "{\"Parameters\": {\"DYNAMODB_ENDPOINT_URL\": \"http://${DDB_CONTAINER_NAME}:${DDB_LOCAL_PORT}\", \"DYNAMODB_TABLE_NAME\": \"${DDB_TABLE_NAME}\"}}" | jq . > ${PATH_TO_ENVVAR}
cd ${CWD}/../provisioning
cdk synth
sam local start-api --template-file cdk.out/ApiStack.template.json --docker-network ${DOCKER_NETWORK_NAME} --env-vars ${PATH_TO_ENVVAR}

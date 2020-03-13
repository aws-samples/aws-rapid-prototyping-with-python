#!/bin/bash
set -e

CWD=$(dirname "${0}")

DDB_CONTAINER_PREFIX=unittestddblocal
DDB_CONTAINER_NAME=${DDB_CONTAINER_PREFIX}$(date "+%Y%m%d%H%M%S")
DDB_LOCAL_PORT=8001
EXISTING_CONTAINERS=$(docker ps -aq --filter name=${DDB_CONTAINER_PREFIX})
PATH_TO_ENVVAR=/tmp/pythonrapidenv.json

docker pull amazon/dynamodb-local

# Lanuch DDB Local
if [ ! "x${EXISTING_CONTAINERS}" = "x" ]; then
  docker stop ${EXISTING_CONTAINERS}
  docker rm ${EXISTING_CONTAINERS}
fi
docker run -d --name ${DDB_CONTAINER_NAME} -p ${DDB_LOCAL_PORT}:8000 amazon/dynamodb-local

# Run py.test
python -m pytest ${CWD}/../tests/ -vv

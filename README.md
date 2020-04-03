## AWS Rapid Prototyping with Python [![CircleCI](https://circleci.com/gh/aws-samples/aws-rapid-prototyping-with-python.svg?style=svg)](https://circleci.com/gh/aws-samples/aws-rapid-prototyping-with-python)

This is a project to experience application development on AWS with the actual minimal implementations!  
It contains:
- Basic 3-tiers serverlss WEB application which depends on:
  - Amazon API Gateway
  - AWS Lambda
  - Amazon DynamoDB
- Unit tests

## Try it out on your local machine

### Prerequisite

- [SAM (Serverless Application Model) CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- Docker
  - for SAM Local
  - for [DynamoDB Local](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html)
    - Both SAM Local and unit tests depend on it
- Python 3.6 or later
  - Specified 3.8 as default
  - You can easily change the version by modifying `pyproject.toml`

### Create virtual environment and install dependencies

This project depends on [`Poetry`](https://python-poetry.org/) to manage the environment and dependencies.  
So first of all, install it using `pip` command.

```sh
$ pip install poetry
```

And then, create its virtual environment and install dependencies.

```sh
$ poetry shell
$ poetry install
```

### Run locally

You can launch the application on your local machine with the following script, it performs:
- Pull the docker image of DynamoDB Local from [dockerhub](https://hub.docker.com/r/amazon/dynamodb-local)
- Create a docker network common between DynamoDB Local and SAM Local if not exists
- Lanuch DynamoDB Local
- Create DynamoDB schema into DynamoDB Local
- Launch application through SAM Local

```sh
$ bash scripts/samlocal.sh
```

### Run unit test

You can run unit test with the following script, it performs:
- Lanuch DynamoDB Local
  - Different container from SAM Local's one
- Run py.test

```sh
bash scripts/unittest.sh
```

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

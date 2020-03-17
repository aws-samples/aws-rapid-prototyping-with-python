## AWS Rapid Prototyping with Python

This is a project to experience application development on AWS with the actual minimal implementations!

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

```sh
$ bash scripts/samlocal.sh
```

### Run unit tests

```sh
bash scripts/unittest.sh
```

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

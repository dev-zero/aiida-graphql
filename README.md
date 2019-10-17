# aiida-graphql

[![Build Status](https://travis-ci.com/dev-zero/aiida-graphql.svg?branch=develop)](https://travis-ci.com/dev-zero/aiida-graphql) [![codecov](https://codecov.io/gh/dev-zero/aiida-graphql/branch/develop/graph/badge.svg)](https://codecov.io/gh/dev-zero/aiida-graphql) [![PyPI](https://img.shields.io/pypi/pyversions/aiida-graphql)](https://pypi.org/project/aiida-graphql/)

Strawberry-based GraphQL Server for AiiDA

Why when there is already the REST API? See https://www.howtographql.com/basics/1-graphql-is-the-better-rest/
... a lot of possible optimizations and fits the graph-based structure of the AiiDA DB a lot better than a REST API.

## Requirements

* Python 3.7+
* https://pypi.org/project/strawberry-graphql/
* https://pypi.org/project/aiida-core/ 1.0.0b6+

For development: https://poetry.eustace.io/

# Usage

## Development

Installing the dependencies:

```bash
git clone https://github.com/dev-zero/aiida-graphql.git
cd aiida-graphql

# for poetry installation use the official documentation
poetry install
```

To run the development server:

```console
$ poetry run strawberry server aiida_graphql.schema
```

then visit http://localhost:8000/graphql with your browser.

Example query:

```graphql
{
  computers {
    uuid
    name
    description
    schedulerType
    transportType
  }
}
```

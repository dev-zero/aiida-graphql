# aiida-graphql

[![Build Status](https://travis-ci.com/dev-zero/aiida-graphql.svg?branch=develop)](https://travis-ci.com/dev-zero/aiida-graphql) [![codecov](https://codecov.io/gh/dev-zero/aiida-graphql/branch/develop/graph/badge.svg)](https://codecov.io/gh/dev-zero/aiida-graphql) [![PyPI](https://img.shields.io/pypi/pyversions/aiida-graphql)](https://pypi.org/project/aiida-graphql/)

Strawberry-based GraphQL Server for AiiDA

Why GraphQL when there is already the REST API? See https://www.howtographql.com/basics/1-graphql-is-the-better-rest/
... a lot of possible optimizations and fits the graph-based structure of the AiiDA DB a lot better than a REST API.

## Requirements

* Python 3.7+
* https://pypi.org/project/strawberry-graphql/ 0.16.7+
* https://pypi.org/project/aiida-core/ 1.0.0b6+

For development: https://poetry.eustace.io/

Why Strawberry for GraphQL? It uses graphql-core v3 (while graphene is still stuck with v2), uses typings and dataclasses for both validation and schema generation. And it uses modern Python to write the schema, in comparison to the [schema-first approach](https://ariadnegraphql.org/).

Why Python 3.7+? It's the future, and for Strawberry. In fact, were it not for a bug in `uvloop` this would be Python 3.8+ (for the walrus operator). And given the timeline these projects are running for, we'll probably see Python 3.9 until people effectively start using it.

Why Poetry? I wanted to get away from `setuptools` and used Poetry already in a [different project](https://github.com/dev-zero/cp2k-input-tools) and liked the virtualenv integration.

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

![Query Screenshot](docs/screenshot.png?raw=true "Query Screenshot")


# Available fields

* node
* calculation
* computer
* user
* singlefile
* gaussian_basissets (only if the [aiida-gaussian-datatypes](https://github.com/dev-zero/aiida-gaussian-datatypes) is installed)

Documentation and schema are embedded in the development server.

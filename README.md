# aiida-graphql

[![Build Status](https://travis-ci.com/dev-zero/aiida-graphql.svg?branch=develop)](https://travis-ci.com/dev-zero/aiida-graphql) [![codecov](https://codecov.io/gh/dev-zero/aiida-graphql/branch/develop/graph/badge.svg)](https://codecov.io/gh/dev-zero/aiida-graphql) [![PyPI](https://img.shields.io/pypi/pyversions/aiida-graphql)](https://pypi.org/project/aiida-graphql/)

Flask-based GraphQL Server for AiiDA

## Requirements

* Python 3.6+
* https://pypi.org/project/Flask-GraphQL/
* https://pypi.org/project/graphene/

For development: https://poetry.eustace.io/

# Usage

## To run the development server

```console
$ FLASK_APP=aiida_graphql.app flask run
```

then visit http://localhost:5000/graphql with your browser.

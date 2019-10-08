
from flask import Flask
from graphene import ObjectType, String, Schema
from flask_graphql import GraphQLView


class Query(ObjectType):
    # this defines a Field `hello` in our Schema with a single Argument `name`
    hello = String(name=String(default_value="stranger"))
    goodbye = String()

    # our Resolver method takes the GraphQL context (root, info) as well as
    # Argument (name) for the Field and returns data for the query Response
    def resolve_hello(root, info, name):
        return f'Hello {name}!'

    def resolve_goodbye(root, info):
        return 'See ya!'


def create_app(path='/graphql', **kwargs):
    app = Flask(__name__)

    app.add_url_rule(path, view_func=GraphQLView.as_view('graphql', schema=Schema(query=Query), graphiql=True, **kwargs))

    return app

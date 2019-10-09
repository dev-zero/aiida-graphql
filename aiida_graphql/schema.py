
import graphene

from aiida.orm.querybuilder import QueryBuilder
from aiida import orm
from aiida import load_profile
load_profile()


class Node(graphene.ObjectType):
    uuid = graphene.ID(required=True)
    ctime = graphene.DateTime(required=True)
    mtime = graphene.DateTime(required=True)


class Query(graphene.ObjectType):
    node = graphene.Field(Node, uuid=graphene.ID(required=True))

    def resolve_node(parent, info, uuid):
        q = QueryBuilder()
        q.append(orm.Node, tag="node")
        q.add_filter(orm.Node, {"uuid": {"==": uuid}})
        q.add_projection("node", "*")
        return q.first()[0]


schema = graphene.Schema(query=Query)

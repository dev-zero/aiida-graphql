from .api.computer import Computer
from .api.node import Node

import typing
from uuid import UUID

import strawberry
from aiida.orm.querybuilder import QueryBuilder
from aiida import orm
from aiida import load_profile

load_profile()


@strawberry.type
class Root:
    @strawberry.field
    def node(self, info, uuid: str) -> Node:
        q = QueryBuilder()
        q.append(orm.Node, filters={"uuid": {"==": uuid}}, project=["*"])
        entry = q.first()

        if entry:
            return Node.from_orm(entry)

        return None

    @strawberry.field
    def computer(self, info, uuid: str) -> typing.Optional[Computer]:
        try:
            UUID(uuid)
        except ValueError:
            raise ValueError("invalid value passed for uuid") from None  # mask original exception completely

        q = QueryBuilder()
        q.append(orm.Computer, filters={"uuid": {"==": uuid}}, project=["*"])
        entry = q.first()

        if entry:
            return Computer.from_orm(entry)

        return None

    @strawberry.field
    def computers(self, info) -> typing.List[Computer]:
        q = QueryBuilder()
        q.append(orm.Computer, project=["*"])
        return [Computer.from_orm(entry) for entry in q.all()]


schema = strawberry.Schema(query=Root)

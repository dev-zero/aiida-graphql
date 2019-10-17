from .api.computer import Computer
from .api.user import User
from .api.node import Node, Calculation

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
    def node(self, info, uuid: strawberry.ID) -> Node:
        q = QueryBuilder()
        q.append(orm.Node, filters={"uuid": {"==": uuid}}, project=["*"])
        entry = q.first()

        if entry:
            return Node.from_orm(entry)

        return None

    @strawberry.field
    def nodes(self, info) -> typing.List[Node]:
        q = QueryBuilder()
        q.append(orm.Node, project=["*"])
        return [Node.from_orm(entry) for entry in q.iterall()]

    @strawberry.field
    def calculation(self, info, uuid: strawberry.ID) -> Calculation:
        try:
            UUID(uuid)
        except ValueError:
            raise ValueError("invalid value passed for uuid") from None  # mask original exception completely

        q = QueryBuilder()
        q.append(orm.Calculation, filters={"uuid": {"==": uuid}}, project=["*"])
        entry = q.first()

        if entry:
            return Calculation.from_orm(entry)

        return None

    @strawberry.field
    def calculations(self, info) -> typing.List[Calculation]:
        q = QueryBuilder()
        q.append(orm.Node, project=["*"])
        return [Calculation.from_orm(entry) for entry in q.iterall()]

    @strawberry.field
    def computer(self, info, uuid: strawberry.ID) -> typing.Optional[Computer]:
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
        # requested_fields = [s.name.value for s in info.field_nodes[0].selection_set.selections]

        q = QueryBuilder()
        q.append(orm.Computer, project=["*"])
        return [Computer.from_orm(entry) for entry in q.iterall()]

    @strawberry.field
    def user(self, info, email: str) -> typing.Optional[User]:
        users = orm.User.objects.find({"email": email})

        if users:
            return User.from_orm(users[0])

        return None

    @strawberry.field
    def users(self, info) -> typing.List[User]:
        return [User.from_orm(u) for u in orm.User.objects.find()]


schema = strawberry.Schema(query=Root)

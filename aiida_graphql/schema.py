import typing
from uuid import UUID

import strawberry
from aiida.plugins.entry_point import get_entry_point_names, load_entry_point
from aiida.orm.querybuilder import QueryBuilder
from aiida import orm
from aiida import load_profile

from .api.computer import Computer
from .api.user import User
from .api.node import Node, BareNode, Calculation, DC_REGISTRY


load_profile()


@strawberry.type
class Root:
    @strawberry.field
    def node(self, info, uuid: strawberry.ID) -> typing.Optional[Node]:
        q = QueryBuilder()
        q.append(orm.Node, filters={"uuid": {"==": uuid}}, project=["*"])
        entry = q.first()

        if entry:
            # TODO: call function to return proper type depending AiiDA node_type, e.g. the generic version of:
            # if entry[0].node_type == "data.gaussian.basisset.BasisSet.":
            #     return GaussianBasisset.from_orm(entry)

            return BareNode.from_orm(entry)

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
        q.append(orm.Calculation, project=["*"])
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

    @classmethod
    def add_field(cls, name, orm_class, data_class):
        """Add a new field (and it's plural form with the given ORM and Dataclass"""

        name = name.replace(".", "_")

        @strawberry.field(name=name)
        def single(self, info, uuid: strawberry.ID) -> typing.Optional[data_class]:
            try:
                UUID(uuid)
            except ValueError:
                raise ValueError("invalid value passed for uuid") from None  # mask original exception completely

            q = QueryBuilder()
            q.append(orm_class, filters={"uuid": {"==": uuid}}, project=["*"])
            entry = q.first()

            if entry:
                return data_class.from_orm(entry)

            return None

        @strawberry.field(name=f"{name}s")
        def multiple(self, info) -> typing.List[data_class]:
            q = QueryBuilder()
            q.append(orm_class, project=["*"])
            return [data_class.from_orm(entry) for entry in q.iterall()]

        setattr(cls, name, single)
        setattr(cls, f"{name}s", multiple)


# PoC for looking up dataclasses on plugins and loading them dynamically
# Limited to aiida.data subclasses/entry point for now
ep_group_name = "aiida.data"
entry_points = get_entry_point_names(ep_group_name)
for registered_entry_point in entry_points:
    try:
        # Limit to the ones in our internal registry.
        # Could also be provided by the plugin or as part of the ORM class
        # Another option would be to look at the schema added for the REST API
        # but sometimes that doesn't give the access and it would be a bit more involved
        # to recover the typing information from that.
        adc = DC_REGISTRY[registered_entry_point]
    except KeyError:
        continue

    print(f"-> Loading dataclass for {ep_group_name}.{registered_entry_point}, to be registered as {registered_entry_point}")
    cls = load_entry_point(ep_group_name, registered_entry_point)
    Root.add_field(registered_entry_point, cls, adc)

schema = strawberry.Schema(query=Root, types=[BareNode])

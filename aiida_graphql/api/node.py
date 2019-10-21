from .user import User

import typing
import dataclasses

import strawberry


@strawberry.interface
class Node:
    uuid: strawberry.ID
    ctime: str
    mtime: str
    label: str
    user: User


@strawberry.type
class BareNode(Node):
    @staticmethod
    def from_orm(ormobj):
        return BareNode(
            uuid=ormobj[0].uuid,
            ctime=ormobj[0].ctime,
            mtime=ormobj[0].mtime,
            label=ormobj[0].label,
            user=User.from_orm(ormobj[0].user),
        )


@strawberry.type
class CalculationAttributes:
    exception: typing.Optional[str] = None
    input_filename: typing.Optional[str] = None
    output_filename: typing.Optional[str] = None
    parser_name: typing.Optional[str] = None
    process_label: typing.Optional[str] = None
    process_state: typing.Optional[str] = None
    sealed: typing.Optional[bool] = None
    withmpi: typing.Optional[bool] = None

    @staticmethod
    def from_orm(ormdict):
        used_attrs = [a.name for a in dataclasses.fields(CalculationAttributes)]
        filtered_dict = {k: v for k, v in ormdict.items() if k in used_attrs}
        return CalculationAttributes(**filtered_dict)


@strawberry.type
class Calculation(Node):
    attributes: CalculationAttributes

    @staticmethod
    def from_orm(ormobj):
        return Calculation(
            uuid=ormobj[0].uuid,
            ctime=ormobj[0].ctime,
            mtime=ormobj[0].mtime,
            label=ormobj[0].label,
            user=User.from_orm(ormobj[0].user),
            attributes=CalculationAttributes.from_orm(ormobj[0].attributes),
        )


@strawberry.type
class Singlefile(Node):
    filename: str

    @staticmethod
    def from_orm(ormobj):
        return Singlefile(
            uuid=ormobj[0].uuid,
            ctime=ormobj[0].ctime,
            mtime=ormobj[0].mtime,
            label=ormobj[0].label,
            filename=ormobj[0].filename,
            user=User.from_orm(ormobj[0].user),
        )


@strawberry.type
class GaussianBasisset(Node):
    name: str
    element: str
    tags: typing.List[str]
    aliases: typing.List[str]
    n_el: int
    version: int

    @staticmethod
    def from_orm(ormobj):
        return GaussianBasisset(
            uuid=ormobj[0].uuid,
            ctime=ormobj[0].ctime,
            mtime=ormobj[0].mtime,
            label=ormobj[0].label,
            name=ormobj[0].name,
            element=ormobj[0].element,
            tags=ormobj[0].tags,
            aliases=ormobj[0].aliases,
            n_el=ormobj[0].n_el,
            version=ormobj[0].version,
            user=User.from_orm(ormobj[0].user),
        )


DC_REGISTRY = {"singlefile": Singlefile, "gaussian.basisset": GaussianBasisset}

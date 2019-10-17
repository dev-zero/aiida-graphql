from .user import User

import typing
import dataclasses

import strawberry


@strawberry.interface
class NodeIface:
    uuid: strawberry.ID
    ctime: str
    mtime: str
    label: str
    user: User


@strawberry.type
class Node(NodeIface):
    @staticmethod
    def from_orm(ormobj):
        return Node(
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
class Calculation(NodeIface):
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

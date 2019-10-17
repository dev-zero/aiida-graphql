import strawberry


@strawberry.type
class Node:
    uuid: strawberry.ID
    ctime: str
    mtime: str
    label: str
    node_type: str

    @staticmethod
    def from_orm(ormobj):
        return ormobj[0]

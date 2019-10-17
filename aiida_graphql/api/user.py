import strawberry


@strawberry.type
class User:
    id: strawberry.ID
    first_name: str
    last_name: str
    full_name: str
    email: str
    institution: str

    @staticmethod
    def from_orm(ormobj):
        return User(
            id=ormobj.id,
            first_name=ormobj.first_name,
            last_name=ormobj.last_name,
            email=ormobj.email,
            institution=ormobj.institution,
            full_name=f"{ormobj.first_name} {ormobj.last_name}",
        )

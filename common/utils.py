from users_service.schema import UserSchema
def get_all_schemas_in_order():
    return [UserSchema]

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d
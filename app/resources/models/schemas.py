from marshmallow import Schema, fields
from .basic import UserRoleEnum, CollaboratorRoleEnum

class BaseSchema(Schema):
    """
        Basic schema that contains all the common fields.
    """
    id = fields.Integer(dump_only=True)

class UserSchema(BaseSchema):
    """
        Schema for the user model.
    """
    name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)
    role = fields.Enum(UserRoleEnum, by_value=False)

class CollaboratorSchema(BaseSchema):
    """
        Schema for the collaborator model.
    """
    name = fields.String(required=True)
    surname = fields.String(required=True)
    date_of_birth = fields.Date(format='%d/%m/%Y', required=True)
    role = fields.Enum(CollaboratorRoleEnum, by_value=False)
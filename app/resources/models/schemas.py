from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError
from .basic import UserRoleEnum

class IntEnumField(fields.Field):
    """
        Custom marshmallow field for the user role enum.
    """
    def __init__(self, enum_class, **kwargs):
        self.enum_class = enum_class
        super().__init__(**kwargs)
        
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value.value

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None
        
        try:
            return self.enum_class(value)
        except ValueError:
            raise ValidationError(f'Invalid {self.enum_class.__name__} value was passed.')

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
    role = IntEnumField(UserRoleEnum)

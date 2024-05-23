from marshmallow import Schema, fields

from .basic import UserRoleEnum, CollaboratorRoleEnum, StorageHistoryTypeEnum

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

class ClientSchema(BaseSchema):
    """
        Schema for the client model.
    """
    name = fields.String(required=True)
    phone_number = fields.String(required=True)
    email = fields.Email(required=True)
    address = fields.String(required=True)

class TruckSchema(BaseSchema):
    """
        Schema for the truck model.
    """
    name = fields.String(required=True)
    plate = fields.String(required=True)
    capacity_kg = fields.Float(required=True)

class MaterialSchema(BaseSchema):
    """
        Schema for the material model.
    """
    name = fields.String(required=True)
    description = fields.String(required=False)
    price_per_kg = fields.Float(required=True)

class MaterialCollectSiteSchema(BaseSchema):
    """
        Schema for the material collect site model.
    """
    neighborhood = fields.String(required=True)
    city = fields.String(required=True)
    uf = fields.String(required=True)

class MaterialCollectionSchema(BaseSchema):
    """
        Schema for the material collection model.
    """
    date = fields.Date(format='%d/%m/%Y', required=True)
    truck_id = fields.Integer(required=True)
    collect_site_id = fields.Integer(required=True)

class MaterialTriageSchema(BaseSchema):
    """
        Schema for the material triage model.
    """
    date = fields.Date(format='%d/%m/%Y', required=True)
    collaborator_id = fields.Integer(required=True)
    material_collection_id = fields.Integer(required=True)
    storage_history_id = fields.Integer(required=True)

class StorageHistorySchema(BaseSchema):
    """
        Schema for the storage history model.
    """
    date = fields.Date(format='%d/%m/%Y', required=True)
    type = fields.Enum(StorageHistoryTypeEnum, by_value=False)
    collaborator_id = fields.Integer(required=True)
    material_id = fields.Integer(required=True)
    quantity_kg = fields.Float(required=True)

class StorageTransactionSchema(BaseSchema):
    """
        Schema for the storage transaction model.
    """
    transaction_id = fields.Integer(required=True)
    storage_history_id = fields.Integer(required=True)

class TransactionSchema(BaseSchema):
    """
        Schema for the transaction model.
    """
    date = fields.Date(format='%d/%m/%Y', required=True)
    client_id = fields.Integer(required=True)
    collaborator_id = fields.Integer(required=True)
    value = fields.Float(required=True)

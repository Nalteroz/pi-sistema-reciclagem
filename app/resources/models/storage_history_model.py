from ..data import system_db
from .basic import BaseModel, StorageHistoryTypeEnum

class StorageHistoryModel(BaseModel):
    __tablename__ = 'storage_history'
    __table_args__ = {"schema": "operation"}

    date = system_db.Column(system_db.DateTime, nullable=False)
    type = system_db.Column(system_db.Enum(StorageHistoryTypeEnum), nullable=False)
    collaborator_id = system_db.Column(system_db.Integer, system_db.ForeignKey('operation.collaborator.id'), nullable=False)
    material_id = system_db.Column(system_db.Integer, system_db.ForeignKey('operation.material.id'), nullable=False)
    quantity_kg = system_db.Column(system_db.Float(), nullable=False)
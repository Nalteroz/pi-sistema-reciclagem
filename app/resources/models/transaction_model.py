from ..data import system_db
from .basic import BaseModel

class TransactionModel(BaseModel):
    __tablename__ = 'transaction'
    __table_args__ = {"schema": "operation"}

    date = system_db.Column(system_db.DateTime, nullable=False)
    client_id = system_db.Column(system_db.Integer, system_db.ForeignKey('operation.client.id'), nullable=False)
    collaborator_id = system_db.Column(system_db.Integer, system_db.ForeignKey('operation.collaborator.id'), nullable=False)
    value = system_db.Column(system_db.Float(), nullable=False)

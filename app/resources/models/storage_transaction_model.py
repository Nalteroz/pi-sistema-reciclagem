from ..data import system_db
from .basic import BaseModel

class StorageTransactionModel(BaseModel):
    __tablename__ = 'storage_transaction'
    __table_args__ = {"schema": "operation"}

    transaction_id = system_db.Column(system_db.Integer, system_db.ForeignKey('operation.transaction.id'), nullable=False)
    storage_history_id = system_db.Column(system_db.Integer, system_db.ForeignKey('operation.storage_history.id'), nullable=False)

    def GetColumnsNames():
        return {
            "transaction_id": "ID da transação comercial",
            "storage_history_id": "ID do histórico do armazém",
        }
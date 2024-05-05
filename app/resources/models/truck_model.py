from ..data import system_db
from .basic import BaseModel

class TruckModel(BaseModel):
    __tablename__ = 'truck'
    __table_args__ = {"schema": "operation"}

    name = system_db.Column(system_db.String(255), nullable=False)
    plate = system_db.Column(system_db.String(255), nullable=False, unique=True)
    capacity_kg = system_db.Column(system_db.Float(), nullable=False)

    def GetColumnsNames():
        return {
            "name": "nome",
            "plate": "placa",
            "capacity_kg": "capacidade (kg)",
        }
from ..data import system_db
from .basic import BaseModel

class TruckModel(BaseModel):
    __tablename__ = 'truck'
    __table_args__ = {"schema": "operation"}

    plate = system_db.Column(system_db.String(255), nullable=False)
    max_load_kg = system_db.Column(system_db.Float(), nullable=False)
from ..data import system_db
from .basic import BaseModel

class MaterialModel(BaseModel):
    __tablename__ = 'material'
    __table_args__ = {"schema": "operation"}

    name = system_db.Column(system_db.String(255), nullable=False)
    description = system_db.Column(system_db.String(255), nullable=True)
    price_per_kg = system_db.Column(system_db.Float(), nullable=False)
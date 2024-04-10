from ..data import system_db
from .basic import BaseModel

class ClientModel(BaseModel):
    __tablename__ = 'client'
    __table_args__ = {"schema": "operation"}

    name = system_db.Column(system_db.String(255), nullable=False)
    phone_number = system_db.Column(system_db.String(255), nullable=False)
    email = system_db.Column(system_db.String(255), nullable=False)
    address = system_db.Column(system_db.String(255), nullable=False)
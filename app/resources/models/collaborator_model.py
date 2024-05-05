from ..data import system_db
from .basic import BaseModel, CollaboratorRoleEnum

class CollaboratorModel(BaseModel):
    __tablename__ = 'collaborator'
    __table_args__ = {"schema": "operation"}

    name = system_db.Column(system_db.String(255), nullable=False)
    surname = system_db.Column(system_db.String(255), nullable=False)
    date_of_birth = system_db.Column(system_db.Date(), nullable=False)
    role = system_db.Column(system_db.Enum(CollaboratorRoleEnum), nullable=False)

    def GetColumnsNames():
        return {
            "name": "nome",
            "surname": "sobrenome",
            "date_of_birth": "data de nascimento",
            "role": "cargo",
        }
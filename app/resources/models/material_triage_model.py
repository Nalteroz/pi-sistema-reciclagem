from ..data import system_db
from .basic import BaseModel

class MaterialTriageModel(BaseModel):
    __tablename__ = 'material_triage'
    __table_args__ = {"schema": "operation"}

    date = system_db.Column(system_db.DateTime, nullable=False)
    collaborator_id = system_db.Column(system_db.Integer, system_db.ForeignKey('operation.collaborator.id'), nullable=False)
    material_collection_id = system_db.Column(system_db.Integer, system_db.ForeignKey('operation.material_collection.id'), nullable=False)
    storage_history_id = system_db.Column(system_db.Integer, system_db.ForeignKey('operation.storage_history.id'), nullable=False)
from ..data import system_db
from .basic import BaseModel

class MaterialCollectionModel(BaseModel):
    __tablename__ = 'material_collection'
    __table_args__ = {"schema": "operation"}

    date = system_db.Column(system_db.DateTime, nullable=False)
    truck_id = system_db.Column(system_db.Integer, system_db.ForeignKey('operation.truck.id'), nullable=False)
    collect_site_id = system_db.Column(system_db.Integer, system_db.ForeignKey('operation.material_collect_site.id'), nullable=False)

    def GetColumnsNames():
        return {
            "date": "data",
            "truck_id": "ID do caminhão",
            "collect_site_id": "ID do local de coleta",
        }
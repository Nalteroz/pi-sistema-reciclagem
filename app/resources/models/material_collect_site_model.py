from ..data import system_db
from .basic import BaseModel

class MaterialCollectSiteModel(BaseModel):
    __tablename__ = 'material_collect_site'
    __table_args__ = {"schema": "operation"}

    neighborhood = system_db.Column(system_db.String(255), nullable=False)
    city = system_db.Column(system_db.String(255), nullable=False)
    uf = system_db.Column(system_db.String(2), nullable=False)

    def GetColumnsNames():
        return {
            "neighborhood": "bairro",
            "city": "cidade",
            "uf": "UF",
        }
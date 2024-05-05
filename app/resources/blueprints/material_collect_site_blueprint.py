from flask import jsonify 
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, current_user

from resources.data import system_db
from resources.models import MaterialCollectSiteModel, MaterialCollectSiteSchema, UserRoleEnum 

MaterialCollectSiteBlueprint = Blueprint('material_collect_site', __name__, url_prefix='/api/material_collect_site')

@MaterialCollectSiteBlueprint.route('/')
class RootMaterialCollectSiteMethodView(MethodView):
    @jwt_required()
    @MaterialCollectSiteBlueprint.response(200, MaterialCollectSiteSchema(many=True))
    def get(self):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get this information.')

        material_collect_sites = MaterialCollectSiteModel.query.all()
        return material_collect_sites

    @jwt_required()
    @MaterialCollectSiteBlueprint.arguments(MaterialCollectSiteSchema)
    @MaterialCollectSiteBlueprint.response(201, MaterialCollectSiteSchema)
    def post(self, new_material_collect_site_data):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get material_collect_sites information.')

        if MaterialCollectSiteModel.query.filter_by(name=new_material_collect_site_data['neighborhood'], surname = new_material_collect_site_data['city']).first():
            abort(409, message='Element already exists. If you want to reactivate and you are an admin, update the element instead.')

        material_collect_sites = MaterialCollectSiteModel(**new_material_collect_site_data) 

        system_db.session.add(material_collect_sites)
        system_db.session.commit()

        return material_collect_sites
    
@MaterialCollectSiteBlueprint.route('/<int:material_collect_site_id>')
class SingleMaterialCollectSiteMethodView(MethodView):
    @jwt_required()
    @MaterialCollectSiteBlueprint.response(200, MaterialCollectSiteSchema)
    def get(self, material_collect_site_id):
        material_collect_site = MaterialCollectSiteModel.query.get(material_collect_site_id)
        if not material_collect_site:
            abort(404, message='material_collect_site not found.')

        return material_collect_site

    @jwt_required()
    @MaterialCollectSiteBlueprint.arguments(MaterialCollectSiteSchema)
    @MaterialCollectSiteBlueprint.response(200, MaterialCollectSiteSchema)
    def put(self, material_collect_site_data, material_collect_site_id):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get material_collect_site information.')

        db_material_collect_site = MaterialCollectSiteModel.query.get(material_collect_site_id)
        if not db_material_collect_site:
            abort(404, message='material_collect_site not found.')

        if 'neighborhood' in material_collect_site_data:
            db_material_collect_site.neighborhood = material_collect_site_data['neighborhood']

        if 'city' in material_collect_site_data:
            db_material_collect_site.city = material_collect_site_data['city']

        if 'uf' in material_collect_site_data:
            db_material_collect_site.uf = material_collect_site_data['uf']

        system_db.session.add(db_material_collect_site)
        system_db.session.commit()

        return material_collect_site_data

    @jwt_required()
    @MaterialCollectSiteBlueprint.response(201, MaterialCollectSiteSchema)
    def delete(self, material_collect_site_id):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get material_collect_site information.')

        db_material_collect_site = MaterialCollectSiteModel.query.get(material_collect_site_id)
        if not db_material_collect_site:
            abort(404, message='material_collect_site not found.')

        system_db.session.delete(db_material_collect_site)
        system_db.session.commit()

        return db_material_collect_site


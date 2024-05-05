from flask import jsonify 
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, current_user

from resources.data import system_db
from resources.models import MaterialCollectionModel, MaterialCollectSiteModel, TruckModel, MaterialCollectionSchema, UserRoleEnum 

MaterialCollectionBlueprint = Blueprint('material_collection', __name__, url_prefix='/api/material_collection')

@MaterialCollectionBlueprint.route('/')
class RootMaterialCollectionMethodView(MethodView):
    @jwt_required()
    @MaterialCollectionBlueprint.response(200, MaterialCollectionSchema(many=True))
    def get(self):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get this information.')

        material_collections = MaterialCollectionModel.query.all()
        return material_collections

    @jwt_required()
    @MaterialCollectionBlueprint.arguments(MaterialCollectionSchema)
    @MaterialCollectionBlueprint.response(201, MaterialCollectionSchema)
    def post(self, new_material_collection_data):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get material_collections information.')

        refered_truck = TruckModel.query.get(new_material_collection_data['truck_id'])
        if not refered_truck:
            abort(404, message='truck not found.')

        refered_collect_site = MaterialCollectSiteModel.query.get(new_material_collection_data['collect_site_id'])
        if not refered_collect_site:
            abort(404, message='collect_site not found.')

        material_collections = MaterialCollectionModel(**new_material_collection_data) 

        system_db.session.add(material_collections)
        system_db.session.commit()

        return material_collections
    
@MaterialCollectionBlueprint.route('/<int:material_collection_id>')
class SingleMaterialCollectionMethodView(MethodView):
    @jwt_required()
    @MaterialCollectionBlueprint.response(200, MaterialCollectionSchema)
    def get(self, material_collection_id):
        material_collection = MaterialCollectionModel.query.get(material_collection_id)
        if not material_collection:
            abort(404, message='material_collection not found.')

        return material_collection

    @jwt_required()
    @MaterialCollectionBlueprint.arguments(MaterialCollectionSchema)
    @MaterialCollectionBlueprint.response(200, MaterialCollectionSchema)
    def put(self, material_collection_data, material_collection_id):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get material_collection information.')

        db_material_collection = MaterialCollectionModel.query.get(material_collection_id)
        if not db_material_collection:
            abort(404, message='material_collection not found.')

        if 'date' in material_collection_data:
            db_material_collection.date = material_collection_data['date']

        if 'truck_id' in material_collection_data:
            db_material_collection.truck_id = material_collection_data['truck_id']

        if 'collect_site_id' in material_collection_data:
            db_material_collection.price_per_kg = material_collection_data['collect_site_id']

        system_db.session.add(db_material_collection)
        system_db.session.commit()

        return material_collection_data

    @jwt_required()
    @MaterialCollectionBlueprint.response(201, MaterialCollectionSchema)
    def delete(self, material_collection_id):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get material_collection information.')

        db_material_collection = MaterialCollectionModel.query.get(material_collection_id)
        if not db_material_collection:
            abort(404, message='material_collection not found.')

        system_db.session.delete(db_material_collection)
        system_db.session.commit()

        return db_material_collection


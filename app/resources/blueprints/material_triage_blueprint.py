from flask import jsonify 
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, current_user

from resources.data import system_db
from resources.models import MaterialTriageModel, TransactionModel, MaterialCollectionModel, StorageTransactionModel, MaterialTriageSchema, UserRoleEnum 

MaterialTriageBlueprint = Blueprint('material_triage', __name__, url_prefix='/api/material_triage')

@MaterialTriageBlueprint.route('/')
class RootMaterialTriageMethodView(MethodView):
    @jwt_required()
    @MaterialTriageBlueprint.response(200, MaterialTriageSchema(many=True))
    def get(self):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get this information.')

        material_triage = MaterialTriageModel.query.all()
        return material_triage

    @jwt_required()
    @MaterialTriageBlueprint.arguments(MaterialTriageSchema)
    @MaterialTriageBlueprint.response(201, MaterialTriageSchema)
    def post(self, new_material_triage_data):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get material_triage information.')

        refered_collaborator = TransactionModel.query.get(new_material_triage_data['collaborator_id'])
        if not refered_collaborator:
            abort(404, message='collaborator not found.')

        refered_material_collection = MaterialCollectionModel.query.get(new_material_triage_data['material_collection_id'])
        if not refered_material_collection:
            abort(404, message='material collection not found.')

        refered_storage_history = StorageTransactionModel.query.get(new_material_triage_data['storage_history_id'])
        if not refered_storage_history:
            abort(404, message='storage history not found.')

        material_triage = MaterialTriageModel(**new_material_triage_data) 

        system_db.session.add(material_triage)
        system_db.session.commit()

        return material_triage
    
@MaterialTriageBlueprint.route('/<int:material_triage_id>')
class SingleMaterialTriageMethodView(MethodView):
    @jwt_required()
    @MaterialTriageBlueprint.response(200, MaterialTriageSchema)
    def get(self, material_triage_id):
        material_triage = MaterialTriageModel.query.get(material_triage_id)
        if not material_triage:
            abort(404, message='material_triage not found.')

        return material_triage

    @jwt_required()
    @MaterialTriageBlueprint.arguments(MaterialTriageSchema)
    @MaterialTriageBlueprint.response(200, MaterialTriageSchema)
    def put(self, material_triage_data, material_triage_id):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get material_triage information.')

        db_material_triage = MaterialTriageModel.query.get(material_triage_id)
        if not db_material_triage:
            abort(404, message='material_triage not found.')

        if 'date' in material_triage_data:
            db_material_triage.date = material_triage_data['date']

        if 'collaborator_id' in material_triage_data:
            db_material_triage.collaborator_id = material_triage_data['collaborator_id']

        if 'material_collection_id' in material_triage_data:
            db_material_triage.material_collection_id = material_triage_data['material_collection_id']

        if 'storage_history_id' in material_triage_data:
            db_material_triage.storage_history_id = material_triage_data['storage_history_id']

        system_db.session.add(db_material_triage)
        system_db.session.commit()

        return material_triage_data

    @jwt_required()
    @MaterialTriageBlueprint.response(201, MaterialTriageSchema)
    def delete(self, material_triage_id):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get material_triage information.')

        db_material_triage = MaterialTriageModel.query.get(material_triage_id)
        if not db_material_triage:
            abort(404, message='material_triage not found.')

        system_db.session.delete(db_material_triage)
        system_db.session.commit()

        return db_material_triage


from flask import jsonify 
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, current_user

from resources.data import system_db
from resources.models import CollaboratorModel, StorageHistoryModel, MaterialModel, StorageHistorySchema, UserRoleEnum 

StorageHistoryBlueprint = Blueprint('storage_history', __name__, url_prefix='/api/storage_history')

@StorageHistoryBlueprint.route('/')
class RootStorageHistoryMethodView(MethodView):
    @jwt_required()
    @StorageHistoryBlueprint.response(200, StorageHistorySchema(many=True))
    def get(self):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get this information.')

        storage_historys = StorageHistoryModel.query.all()
        return storage_historys

    @jwt_required()
    @StorageHistoryBlueprint.arguments(StorageHistorySchema)
    @StorageHistoryBlueprint.response(201, StorageHistorySchema)
    def post(self, new_storage_history_data):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get storage_historys information.')

        refered_collaborator = CollaboratorModel.query.get(new_storage_history_data['collaborator_id'])
        if not refered_collaborator:
            abort(404, message='collaborator not found.')

        refered_material = MaterialModel.query.get(new_storage_history_data['material_id'])
        if not refered_material:
            abort(404, message='material not found.')

        storage_historys = StorageHistoryModel(**new_storage_history_data) 

        system_db.session.add(storage_historys)
        system_db.session.commit()

        return storage_historys
    
@StorageHistoryBlueprint.route('/<int:storage_history_id>')
class SingleStorageHistoryMethodView(MethodView):
    @jwt_required()
    @StorageHistoryBlueprint.response(200, StorageHistorySchema)
    def get(self, storage_history_id):
        storage_history = StorageHistoryModel.query.get(storage_history_id)
        if not storage_history:
            abort(404, message='storage_history not found.')

        return storage_history

    @jwt_required()
    @StorageHistoryBlueprint.arguments(StorageHistorySchema)
    @StorageHistoryBlueprint.response(200, StorageHistorySchema)
    def put(self, storage_history_data, storage_history_id):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get storage_history information.')

        db_storage_history = StorageHistoryModel.query.get(storage_history_id)
        if not db_storage_history:
            abort(404, message='storage_history not found.')

        if 'date' in storage_history_data:
            db_storage_history.date = storage_history_data['date']

        if 'type' in storage_history_data:
            db_storage_history.type = storage_history_data['type']

        if 'collaborator_id' in storage_history_data:
            db_storage_history.collaborator_id = storage_history_data['collaborator_id']

        if 'material_id' in storage_history_data:
            db_storage_history.material_id = storage_history_data['material_id']

        if 'quantity_kg' in storage_history_data:
            db_storage_history.quantity_kg = storage_history_data['quantity_kg']

        system_db.session.add(db_storage_history)
        system_db.session.commit()

        return storage_history_data

    @jwt_required()
    @StorageHistoryBlueprint.response(201, StorageHistorySchema)
    def delete(self, storage_history_id):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get storage_history information.')

        db_storage_history = StorageHistoryModel.query.get(storage_history_id)
        if not db_storage_history:
            abort(404, message='storage_history not found.')

        system_db.session.delete(db_storage_history)
        system_db.session.commit()

        return db_storage_history

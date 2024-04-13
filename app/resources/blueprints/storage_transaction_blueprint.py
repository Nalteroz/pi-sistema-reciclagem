from flask import jsonify 
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, current_user

from resources.data import system_db
from resources.models import StorageTransactionModel, TransactionModel, StorageHistoryModel, StorageTransactionSchema, UserRoleEnum 

StorageTransactionBlueprint = Blueprint('storage_transaction', __name__, url_prefix='/storage_transaction')

@StorageTransactionBlueprint.route('/')
class RootStorageTransactionMethodView(MethodView):
    @jwt_required()
    @StorageTransactionBlueprint.response(200, StorageTransactionSchema(many=True))
    def get(self):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get this information.')

        storage_transactions = StorageTransactionModel.query.all()
        return storage_transactions

    @jwt_required()
    @StorageTransactionBlueprint.arguments(StorageTransactionSchema)
    @StorageTransactionBlueprint.response(201, StorageTransactionSchema)
    def post(self, new_storage_transaction_data):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get storage_transactions information.')

        refered_transaction = TransactionModel.query.get(new_storage_transaction_data['transaction_id'])
        if not refered_transaction:
            abort(404, message='transaction not found.')

        refered_storage_history = StorageHistoryModel.query.get(new_storage_transaction_data['storage_history_id'])
        if not refered_storage_history:
            abort(404, message='storage_history not found.')

        storage_transactions = StorageTransactionModel(**new_storage_transaction_data) 

        system_db.session.add(storage_transactions)
        system_db.session.commit()

        return storage_transactions
    
@StorageTransactionBlueprint.route('/<int:storage_transaction_id>')
class SingleStorageTransactionMethodView(MethodView):
    @jwt_required()
    @StorageTransactionBlueprint.response(200, StorageTransactionSchema)
    def get(self, storage_transaction_id):
        storage_transaction = StorageTransactionModel.query.get(storage_transaction_id)
        if not storage_transaction:
            abort(404, message='storage_transaction not found.')

        return storage_transaction

    @jwt_required()
    @StorageTransactionBlueprint.arguments(StorageTransactionSchema)
    @StorageTransactionBlueprint.response(200, StorageTransactionSchema)
    def put(self, storage_transaction_data, storage_transaction_id):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get storage_transaction information.')

        db_storage_transaction = StorageTransactionModel.query.get(storage_transaction_id)
        if not db_storage_transaction:
            abort(404, message='storage_transaction not found.')

        if 'transaction_id' in storage_transaction_data:
            db_storage_transaction.transaction_id = storage_transaction_data['transaction_id']

        if 'storage_history_id' in storage_transaction_data:
            db_storage_transaction.storage_history_id = storage_transaction_data['storage_history_id']

        system_db.session.add(db_storage_transaction)
        system_db.session.commit()

        return storage_transaction_data

    @jwt_required()
    @StorageTransactionBlueprint.response(201, StorageTransactionSchema)
    def delete(self, storage_transaction_id):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get storage_transaction information.')

        db_storage_transaction = StorageTransactionModel.query.get(storage_transaction_id)
        if not db_storage_transaction:
            abort(404, message='storage_transaction not found.')

        system_db.session.delete(db_storage_transaction)
        system_db.session.commit()

        return db_storage_transaction

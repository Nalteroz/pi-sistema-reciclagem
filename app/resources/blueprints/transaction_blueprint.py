from flask import jsonify 
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, current_user

from resources.data import system_db
from resources.models import TransactionModel, ClientModel, CollaboratorModel, TransactionSchema, UserRoleEnum 

TransactionBlueprint = Blueprint('transaction', __name__, url_prefix='/api/transaction')

@TransactionBlueprint.route('/')
class RootTransactionMethodView(MethodView):
    @jwt_required()
    @TransactionBlueprint.response(200, TransactionSchema(many=True))
    def get(self):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get this information.')

        transactions = TransactionModel.query.all()
        return transactions

    @jwt_required()
    @TransactionBlueprint.arguments(TransactionSchema)
    @TransactionBlueprint.response(201, TransactionSchema)
    def post(self, new_transaction_data):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get transactions information.')

        refered_collaborator = CollaboratorModel.query.get(new_transaction_data['collaborator_id'])
        if not refered_collaborator:
            abort(404, message='collaborator not found.')

        refered_client = ClientModel.query.get(new_transaction_data['client_id'])
        if not refered_client:
            abort(404, message='material not found.')

        transactions = TransactionModel(**new_transaction_data) 

        system_db.session.add(transactions)
        system_db.session.commit()

        return transactions
    
@TransactionBlueprint.route('/<int:transaction_id>')
class SingleTransactionMethodView(MethodView):
    @jwt_required()
    @TransactionBlueprint.response(200, TransactionSchema)
    def get(self, transaction_id):
        transaction = TransactionModel.query.get(transaction_id)
        if not transaction:
            abort(404, message='transaction not found.')

        return transaction

    @jwt_required()
    @TransactionBlueprint.arguments(TransactionSchema)
    @TransactionBlueprint.response(200, TransactionSchema)
    def put(self, transaction_data, transaction_id):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get transaction information.')

        db_transaction = TransactionModel.query.get(transaction_id)
        if not db_transaction:
            abort(404, message='transaction not found.')

        if 'date' in transaction_data:
            db_transaction.date = transaction_data['date']

        if 'client_id' in transaction_data:
            db_transaction.client_id = transaction_data['client_id']

        if 'collaborator_id' in transaction_data:
            db_transaction.collaborator_id = transaction_data['collaborator_id']

        if 'value' in transaction_data:
            db_transaction.value = transaction_data['value']

        system_db.session.add(db_transaction)
        system_db.session.commit()

        return transaction_data

    @jwt_required()
    @TransactionBlueprint.response(201, TransactionSchema)
    def delete(self, transaction_id):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get transaction information.')

        db_transaction = TransactionModel.query.get(transaction_id)
        if not db_transaction:
            abort(404, message='transaction not found.')

        system_db.session.delete(db_transaction)
        system_db.session.commit()

        return db_transaction

from flask import jsonify 
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, current_user

from resources.data import system_db
from resources.models import ClientModel, ClientSchema, UserRoleEnum 

ClientBlueprint = Blueprint('client', __name__, url_prefix='/client')

@ClientBlueprint.route('/')
class RootClientMethodView(MethodView):
    @jwt_required()
    @ClientBlueprint.response(200, ClientSchema(many=True))
    def get(self):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get this information.')

        clients = ClientModel.query.all()
        return clients

    @jwt_required()
    @ClientBlueprint.arguments(ClientSchema)
    @ClientBlueprint.response(201, ClientSchema)
    def post(self, new_client_data):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get clients information.')

        if ClientModel.query.filter_by(email=new_client_data['email']).first():
            abort(409, message='Element already exists. If you want to reactivate and you are an admin, update the element instead.')

        clients = ClientModel(**new_client_data) 

        system_db.session.add(clients)
        system_db.session.commit()

        return clients
    
@ClientBlueprint.route('/<int:client_id>')
class SingleClientMethodView(MethodView):
    @jwt_required()
    @ClientBlueprint.response(200, ClientSchema)
    def get(self, client_id):
        client = ClientModel.query.get(client_id)
        if not client:
            abort(404, message='client not found.')

        return client

    @jwt_required()
    @ClientBlueprint.arguments(ClientSchema)
    @ClientBlueprint.response(200, ClientSchema)
    def put(self, client_data, client_id):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get client information.')

        db_client = ClientModel.query.get(client_id)
        if not db_client:
            abort(404, message='client not found.')

        if 'name' in client_data:
            db_client.name = client_data['name']

        if 'phone_number' in client_data:
            db_client.phone_number = client_data['phone_number']

        if 'email' in client_data:
            db_client.email = client_data['email']

        if 'address' in client_data:
            db_client.address = client_data['address']

        system_db.session.add(db_client)
        system_db.session.commit()

        return client_data

    @jwt_required()
    @ClientBlueprint.response(201, ClientSchema)
    def delete(self, client_id):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get client information.')

        db_client = ClientModel.query.get(client_id)
        if not db_client:
            abort(404, message='client not found.')

        system_db.session.delete(db_client)
        system_db.session.commit()

        return db_client


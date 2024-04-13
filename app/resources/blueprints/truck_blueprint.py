from flask import jsonify 
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, current_user

from resources.data import system_db
from resources.models import TruckModel, TruckSchema, UserRoleEnum 

TruckBlueprint = Blueprint('truck', __name__, url_prefix='/truck')

@TruckBlueprint.route('/')
class RootTruckMethodView(MethodView):
    @jwt_required()
    @TruckBlueprint.response(200, TruckSchema(many=True))
    def get(self):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get collaborators information.')

        trucks = TruckModel.query.all()
        return trucks

    @jwt_required()
    @TruckBlueprint.arguments(TruckSchema)
    @TruckBlueprint.response(201, TruckSchema)
    def post(self, new_truck_data):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get trucks information.')

        if TruckModel.query.filter_by(plate=new_truck_data['plate']).first():
            abort(409, message='Truck already exists. If you want to reactivate and you are an admin, update the truck instead.')

        trucks = TruckModel(**new_truck_data) 

        system_db.session.add(trucks)
        system_db.session.commit()

        return trucks
    
@TruckBlueprint.route('/<int:truck_id>')
class SingleTruckMethodView(MethodView):
    @jwt_required()
    @TruckBlueprint.response(200, TruckSchema)
    def get(self, truck_id):
        """
            Return a single truck information.
        """
        truck = TruckModel.query.get(truck_id)
        if not truck:
            abort(404, message='Truck not found.')

        return truck

    @jwt_required()
    @TruckBlueprint.arguments(TruckSchema)
    @TruckBlueprint.response(200, TruckSchema)
    def put(self, truck_data, truck_id):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get truck information.')

        db_truck = TruckModel.query.get(truck_id)
        if not db_truck:
            abort(404, message='Truck not found.')

        if 'name' in truck_data:
            db_truck.name = truck_data['name']

        if 'plate' in truck_data:
            db_truck.plate = truck_data['plate']

        if 'capacity_kg' in truck_data:
            db_truck.capacity_kg = truck_data['capacity_kg']

        system_db.session.add(db_truck)
        system_db.session.commit()

        return truck_data

    @jwt_required()
    @TruckBlueprint.response(201, TruckSchema)
    def delete(self, truck_id):
        if current_user.role != UserRoleEnum.ADMIN:
            abort(403, message='You are not an admin, or are not allowed get truck information.')

        db_truck = TruckModel.query.get(truck_id)
        if not db_truck:
            abort(404, message='Truck not found.')

        system_db.session.delete(db_truck)
        system_db.session.commit()

        return db_truck

